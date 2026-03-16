import json
import unittest

import boxbotapi
from boxbotapi import configs as cfg
from boxbotapi.bot import HTTPResponse


class MockClient:
    def __init__(self) -> None:
        self.calls = []

    def Do(self, req):
        self.calls.append(req)
        if req.url.endswith("/getMe"):
            body = {
                "ok": True,
                "result": {
                    "user_id": "bot_1",
                    "name": "mybot",
                },
            }
            return HTTPResponse(status_code=200, status="OK", body=json.dumps(body).encode("utf-8"))

        if req.url.endswith("/sendMessage"):
            body = {
                "ok": True,
                "result": {
                    "message_id": "m1",
                    "text": "hello",
                    "chat": {
                        "id": "chat_1",
                        "type": "private",
                    },
                },
            }
            return HTTPResponse(status_code=200, status="OK", body=json.dumps(body).encode("utf-8"))

        if req.url.endswith("/getUpdates"):
            body = {
                "ok": True,
                "result": [
                    {
                        "id": 10,
                        "message": {
                            "message_id": "m2",
                            "text": "ping",
                            "chat": {
                                "id": "chat_1",
                                "type": "private",
                            },
                        },
                    }
                ],
            }
            return HTTPResponse(status_code=200, status="OK", body=json.dumps(body).encode("utf-8"))

        if req.url.endswith("/bad"):
            return HTTPResponse(status_code=500, status="Internal Server Error", body=b"{}")

        return HTTPResponse(status_code=404, status="Not Found", body=b"{}")


class Req:
    def __init__(self, method: str, body):
        self.method = method
        self.body = body


class TestBot(unittest.TestCase):
    def setUp(self) -> None:
        self._orig_endpoint = cfg.APIEndpoint

    def tearDown(self) -> None:
        cfg.APIEndpoint = self._orig_endpoint

    def test_new_bot_api_with_client(self) -> None:
        bot = boxbotapi.NewBotAPIWithClient("token_x", cfg.APIEndpoint, MockClient())
        self.assertEqual("bot_1", bot.Self.UserId)
        self.assertEqual("mybot", bot.Self.Name)

    def test_send_message(self) -> None:
        bot = boxbotapi.NewBotAPIWithClient("token_x", cfg.APIEndpoint, MockClient())
        msg = boxbotapi.NewMessage("chat_1", "private", "hello")
        result = bot.Send(msg)

        self.assertEqual("m1", result.MessageID)
        self.assertEqual("hello", result.Text)
        self.assertEqual("chat_1", result.Chat.ID)

    def test_get_updates(self) -> None:
        bot = boxbotapi.NewBotAPIWithClient("token_x", cfg.APIEndpoint, MockClient())
        updates = bot.GetUpdates(boxbotapi.NewUpdate(0))

        self.assertEqual(1, len(updates))
        self.assertEqual(10, updates[0].Id)
        self.assertEqual("ping", updates[0].Message.Text)

    def test_make_request_non_200(self) -> None:
        bot = boxbotapi.NewBotAPIWithClient("token_x", cfg.APIEndpoint, MockClient())
        with self.assertRaises(boxbotapi.Error):
            bot.MakeRequest("bad", boxbotapi.Params())

    def test_escape_text(self) -> None:
        self.assertEqual("\\_x\\_", boxbotapi.EscapeText(boxbotapi.ModeMarkdown, "_x_"))
        self.assertEqual("&lt;b&gt;", boxbotapi.EscapeText(boxbotapi.ModeHTML, "<b>"))

    def test_handle_update(self) -> None:
        bot = boxbotapi.NewBotAPIWithClient("token_x", cfg.APIEndpoint, MockClient())
        update = bot.HandleUpdate(Req("POST", {"id": 7, "message": {"text": "x", "chat": {"id": "c1", "type": "private"}}}))
        self.assertEqual(7, update.Id)

        with self.assertRaises(ValueError):
            bot.HandleUpdate(Req("GET", {}))

    def test_set_host(self) -> None:
        boxbotapi.SetHost("https://example.com")
        self.assertEqual("https://example.com/openapi/bot%s/%s", cfg.APIEndpoint)


if __name__ == "__main__":
    unittest.main()
