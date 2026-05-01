from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Protocol, runtime_checkable

from .params import Params
from .types import InlineKeyboardMarkup

APIEndpoint = "https://open.debox.pro/openapi/%s"
Debug = False
MessageListener = False

ChatTyping = "typing"

ErrAPIForbidden = "forbidden"

ModeMarkdown = "Markdown"
ModeMarkdownV2 = "MarkdownV2"
ModeHTML = "HTML"
ModeVideo = "video"
ModeImage = "image"
ModeFile = "file"
ModeRichText = "richtext"

UpdateTypeMessage = "message"

ErrBadURL = "bad or empty url"


@runtime_checkable
class Chattable(Protocol):
    def params(self) -> Params:
        ...

    def method(self) -> str:
        ...


@dataclass
class CloseConfig:
    def method(self) -> str:
        return "close"

    def params(self) -> Params:
        return Params()


@dataclass
class BaseChat:
    ChatID: str = ""
    ChatType: str = ""
    ChannelUsername: str = ""
    ReplyMarkup: object = None

    def params(self) -> Params:
        params = Params()
        params.AddFirstValid("chat_id", self.ChatID, self.ChannelUsername)
        params.AddFirstValid("chat_type", self.ChatType, self.ChannelUsername)
        params.AddInterface("reply_markup", self.ReplyMarkup)
        return params


@dataclass
class BaseEdit:
    ChatID: str = ""
    ChatType: str = ""
    ChannelUsername: str = ""
    MessageID: str = ""
    InlineMessageID: str = ""
    ReplyMarkup: Optional[InlineKeyboardMarkup] = None

    def params(self) -> Params:
        params = Params()
        if self.InlineMessageID:
            params["inline_message_id"] = self.InlineMessageID
        else:
            params.AddFirstValid("chat_id", self.ChatID, self.ChannelUsername)
            params.AddFirstValid("chat_type", self.ChatType, self.ChannelUsername)
            params.AddFirstValid("message_id", self.MessageID)
        params.AddInterface("reply_markup", self.ReplyMarkup)
        return params


@dataclass
class MessageConfig:
    BaseChat: BaseChat = field(default_factory=BaseChat)
    Text: str = ""
    ParseMode: str = ""

    @property
    def ReplyMarkup(self) -> object:
        return self.BaseChat.ReplyMarkup

    @ReplyMarkup.setter
    def ReplyMarkup(self, value: object) -> None:
        self.BaseChat.ReplyMarkup = value

    @property
    def ChatID(self) -> str:
        return self.BaseChat.ChatID

    @ChatID.setter
    def ChatID(self, value: str) -> None:
        self.BaseChat.ChatID = value

    @property
    def ChatType(self) -> str:
        return self.BaseChat.ChatType

    @ChatType.setter
    def ChatType(self, value: str) -> None:
        self.BaseChat.ChatType = value

    @property
    def ChannelUsername(self) -> str:
        return self.BaseChat.ChannelUsername

    @ChannelUsername.setter
    def ChannelUsername(self, value: str) -> None:
        self.BaseChat.ChannelUsername = value

    def params(self) -> Params:
        params = self.BaseChat.params()
        params.AddNonEmpty("text", self.Text)
        params.AddNonEmpty("parse_mode", self.ParseMode)
        return params

    def method(self) -> str:
        return "bot/sendMessage"


@dataclass
class MessageToFansConfig:
    BaseChat: BaseChat = field(default_factory=BaseChat)
    Text: str = ""
    ParseMode: str = ""

    @property
    def ReplyMarkup(self) -> object:
        return self.BaseChat.ReplyMarkup

    @ReplyMarkup.setter
    def ReplyMarkup(self, value: object) -> None:
        self.BaseChat.ReplyMarkup = value

    @property
    def ChatID(self) -> str:
        return self.BaseChat.ChatID

    @ChatID.setter
    def ChatID(self, value: str) -> None:
        self.BaseChat.ChatID = value

    @property
    def ChatType(self) -> str:
        return self.BaseChat.ChatType

    @ChatType.setter
    def ChatType(self, value: str) -> None:
        self.BaseChat.ChatType = value

    @property
    def ChannelUsername(self) -> str:
        return self.BaseChat.ChannelUsername

    @ChannelUsername.setter
    def ChannelUsername(self, value: str) -> None:
        self.BaseChat.ChannelUsername = value

    def params(self) -> Params:
        params = self.BaseChat.params()
        params.AddNonEmpty("text", self.Text)
        params.AddNonEmpty("parse_mode", self.ParseMode)
        return params

    def method(self) -> str:
        return "bot/sendMessageToFans"


@dataclass
class EditMessageTextConfig:
    BaseEdit: BaseEdit = field(default_factory=BaseEdit)
    Text: str = ""
    ParseMode: str = ""

    @property
    def ReplyMarkup(self) -> Optional[InlineKeyboardMarkup]:
        return self.BaseEdit.ReplyMarkup

    @ReplyMarkup.setter
    def ReplyMarkup(self, value: Optional[InlineKeyboardMarkup]) -> None:
        self.BaseEdit.ReplyMarkup = value

    @property
    def ChatID(self) -> str:
        return self.BaseEdit.ChatID

    @ChatID.setter
    def ChatID(self, value: str) -> None:
        self.BaseEdit.ChatID = value

    @property
    def ChatType(self) -> str:
        return self.BaseEdit.ChatType

    @ChatType.setter
    def ChatType(self, value: str) -> None:
        self.BaseEdit.ChatType = value

    @property
    def ChannelUsername(self) -> str:
        return self.BaseEdit.ChannelUsername

    @ChannelUsername.setter
    def ChannelUsername(self, value: str) -> None:
        self.BaseEdit.ChannelUsername = value

    @property
    def MessageID(self) -> str:
        return self.BaseEdit.MessageID

    @MessageID.setter
    def MessageID(self, value: str) -> None:
        self.BaseEdit.MessageID = value

    @property
    def InlineMessageID(self) -> str:
        return self.BaseEdit.InlineMessageID

    @InlineMessageID.setter
    def InlineMessageID(self, value: str) -> None:
        self.BaseEdit.InlineMessageID = value

    def params(self) -> Params:
        params = self.BaseEdit.params()
        params["text"] = self.Text
        params.AddNonEmpty("parse_mode", self.ParseMode)
        return params

    def method(self) -> str:
        return "bot/editMessageText"


@dataclass
class UpdateConfig:
    Offset: int = 0
    Limit: int = 0
    Timeout: int = 0
    AllowedUpdates: List[str] = field(default_factory=list)

    def method(self) -> str:
        return "bot/getUpdates"

    def params(self) -> Params:
        params = Params()
        params.AddNonZero("offset", self.Offset)
        params.AddNonZero("limit", self.Limit)
        params.AddNonZero("timeout", self.Timeout)
        params.AddInterface("allowed_updates", self.AllowedUpdates)
        return params


@dataclass
class CallbackConfig:
    CallbackQueryID: str = ""
    Text: str = ""
    ShowAlert: bool = False
    URL: str = ""
    CacheTime: int = 0

    def method(self) -> str:
        return "answerCallbackQuery"

    def params(self) -> Params:
        params = Params()
        params["callback_query_id"] = self.CallbackQueryID
        params.AddNonEmpty("text", self.Text)
        params.AddBool("show_alert", self.ShowAlert)
        params.AddNonEmpty("url", self.URL)
        params.AddNonZero("cache_time", self.CacheTime)
        return params
