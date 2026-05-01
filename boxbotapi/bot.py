from __future__ import annotations

import json
import logging
import hashlib
import random
import threading
import time
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional, Protocol

from . import configs as cfg
from .params import Params
from .types import APIResponse, Error, Message, Update, UpdatesChannel, User


class HTTPClient(Protocol):
    def Do(self, req: "HTTPRequest") -> "HTTPResponse":
        ...


@dataclass
class HTTPRequest:
    method: str
    url: str
    data: Optional[bytes] = None
    headers: Dict[str, str] = None


@dataclass
class HTTPResponse:
    status_code: int
    status: str
    body: bytes


class DefaultHTTPClient:
    def Do(self, req: HTTPRequest) -> HTTPResponse:
        headers = req.headers or {}
        request = urllib.request.Request(
            url=req.url,
            data=req.data,
            headers=headers,
            method=req.method,
        )
        with urllib.request.urlopen(request, timeout=60) as resp:
            return HTTPResponse(
                status_code=resp.status,
                status=getattr(resp, "reason", "OK"),
                body=resp.read(),
            )


class BotAPI:
    def __init__(self, token: str, apiSecret: str, apiEndpoint: str, client: Optional[HTTPClient] = None):
        self.Token = token
        self.ApiSecret = apiSecret
        self.Debug = False
        self.Buffer = 100
        self.Self = User()
        self.Client: HTTPClient = client if client is not None else DefaultHTTPClient()
        self._shutdown = threading.Event()
        self.apiEndpoint = apiEndpoint

    def SetAPIEndpoint(self, apiEndpoint: str) -> None:
        self.apiEndpoint = apiEndpoint

    def MakeRequest(self, endpoint: str, params: Optional[Params]) -> APIResponse:
        params = params or Params()
        if cfg.Debug:
            logging.info("Endpoint: %s, params: %s", endpoint, params)

        method = self.apiEndpoint % endpoint
        encoded = urllib.parse.urlencode(dict(params)).encode("utf-8")
        nonce, timestamp, signature = self.getSignature()
        req = HTTPRequest(
            method="POST",
            url=method,
            data=encoded,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "X-API-KEY": self.Token,
                "nonce": nonce,
                "timestamp": timestamp,
                "signature": signature,
                "X-Request-Id": str(uuid.uuid4()),
            },
        )

        try:
            resp = self.Client.Do(req)
        except Exception as exc:
            raise exc

        if resp.status_code != 200:
            raise Error(Code=resp.status_code, Message=resp.status)

        api_resp = self.decodeAPIResponse(resp.body)

        if cfg.Debug:
            logging.info("Endpoint: %s, response: %s", endpoint, resp.body.decode("utf-8", "ignore"))

        if not api_resp.Ok:
            params_obj = api_resp.Parameters if api_resp.Parameters is not None else None
            raise Error(
                Code=api_resp.ErrorCode,
                Message=api_resp.Message,
                ResponseParameters=params_obj if params_obj is not None else Error().ResponseParameters,
            )

        return api_resp

    def getSignature(self) -> tuple[str, str, str]:
        nonce = str(random.randint(0, 2**31 - 1))
        timestamp = str(int(time.time()))
        signature = hashlib.sha1(f"{self.ApiSecret}{nonce}{timestamp}".encode("utf-8")).hexdigest()
        return nonce, timestamp, signature

    def decodeAPIResponse(self, responseBody: bytes) -> APIResponse:
        data = json.loads(responseBody.decode("utf-8"))
        return APIResponse.from_json_dict(data)

    def GetMe(self) -> User:
        resp = self.MakeRequest("bot/getMe", None)
        user = User.from_dict(resp.Result)
        return user if user is not None else User()

    def IsMessageToMe(self, message: Message) -> bool:
        return ("@" + self.Self.Name) in message.Text

    def Request(self, c: cfg.Chattable) -> APIResponse:
        return self.MakeRequest(c.method(), c.params())

    def Send(self, c: cfg.Chattable) -> Message:
        resp = self.Request(c)
        message = Message.from_dict(resp.Result)
        return message if message is not None else Message()

    def GetUpdates(self, config: cfg.UpdateConfig) -> list[Update]:
        resp = self.Request(config)
        updates_raw = resp.Result if isinstance(resp.Result, list) else []
        updates: list[Update] = []
        for item in updates_raw:
            update = Update.from_dict(item)
            if update is not None:
                updates.append(update)
        return updates

    def GetUpdatesChan(self, config: cfg.UpdateConfig) -> Iterable[Update]:
        if not cfg.MessageListener:
            return iter(())

        def _iter() -> Iterable[Update]:
            while not self._shutdown.is_set():
                try:
                    updates = self.GetUpdates(config)
                except Exception:
                    continue
                for update in updates:
                    if update.Id >= config.Offset:
                        yield update

        return _iter()

    def StopReceivingUpdates(self) -> None:
        self._shutdown.set()

    def ListenForWebhook(self, pattern: str) -> UpdatesChannel:
        _ = pattern
        return UpdatesChannel()

    def ListenForWebhookRespReqFormat(self, w: Any, r: Any) -> UpdatesChannel:
        _ = w
        ch = UpdatesChannel()
        update = self.HandleUpdate(r)
        ch.append(update)
        return ch

    def HandleUpdate(self, r: Any) -> Update:
        method = getattr(r, "method", "")
        if method != "POST":
            raise ValueError("wrong HTTP method required POST")

        body = getattr(r, "body", None)
        if isinstance(body, (bytes, bytearray)):
            payload = json.loads(body.decode("utf-8"))
        elif isinstance(body, str):
            payload = json.loads(body)
        elif isinstance(body, dict):
            payload = body
        else:
            raise ValueError("invalid request body")

        update = Update.from_dict(payload)
        if update is None:
            raise ValueError("invalid update payload")
        return update


def SetHost(host: str) -> None:
    if host:
        cfg.APIEndpoint = f"{host}/openapi/%s"
    else:
        logging.warning("SetHost error,host is empty,use the default host now")


def NewBotAPI(token: str, apiSecret: str) -> BotAPI:
    return NewBotAPIWithClient(token, apiSecret, cfg.APIEndpoint, DefaultHTTPClient())


def NewBotAPIWithAPIEndpoint(token: str, apiSecret: str, apiEndpoint: str) -> BotAPI:
    return NewBotAPIWithClient(token, apiSecret, apiEndpoint, DefaultHTTPClient())


def NewBotAPIWithClient(token: str, apiSecret: str, apiEndpoint: str, client: Optional[HTTPClient]) -> BotAPI:
    bot = BotAPI(token=token, apiSecret=apiSecret, apiEndpoint=apiEndpoint, client=client)
    bot.Self = bot.GetMe()
    return bot


def EscapeText(parseMode: str, text: str) -> str:
    if parseMode == cfg.ModeHTML:
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if parseMode == cfg.ModeMarkdown:
        return (
            text.replace("_", "\\_")
            .replace("*", "\\*")
            .replace("`", "\\`")
            .replace("[", "\\[")
        )
    if parseMode == cfg.ModeMarkdownV2:
        pairs = [
            ("_", "\\_"),
            ("*", "\\*"),
            ("[", "\\["),
            ("]", "\\]"),
            ("(", "\\("),
            (")", "\\)"),
            ("~", "\\~"),
            ("`", "\\`"),
            (">", "\\>"),
            ("#", "\\#"),
            ("+", "\\+"),
            ("-", "\\-"),
            ("=", "\\="),
            ("|", "\\|"),
            ("{", "\\{"),
            ("}", "\\}"),
            (".", "\\."),
            ("!", "\\!"),
        ]
        out = text
        for src, dst in pairs:
            out = out.replace(src, dst)
        return out
    return ""
