from __future__ import annotations

import datetime as _dt
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ResponseParameters:
    MigrateToChatID: int = 0
    RetryAfter: int = 0


@dataclass
class APIResponse:
    Ok: bool = False
    Result: Any = None
    ErrorCode: int = 0
    Message: str = ""
    Parameters: Optional[ResponseParameters] = None

    @classmethod
    def from_json_dict(cls, data: Dict[str, Any]) -> "APIResponse":
        params = data.get("parameters")
        parsed_params = None
        if isinstance(params, dict):
            parsed_params = ResponseParameters(
                MigrateToChatID=params.get("migrate_to_chat_id", 0),
                RetryAfter=params.get("retry_after", 0),
            )
        return cls(
            Ok=bool(data.get("ok", False)),
            Result=data.get("result"),
            ErrorCode=int(data.get("error_code", 0) or 0),
            Message=str(data.get("message", "") or ""),
            Parameters=parsed_params,
        )


@dataclass
class Error(Exception):
    Code: int = 0
    Message: str = ""
    ResponseParameters: ResponseParameters = field(default_factory=ResponseParameters)
    HTTPCode: int = 0
    RequestID: str = ""

    def __str__(self) -> str:
        return self.Message

    def String(self) -> str:
        return json.dumps(
            {
                "errorCode": self.Code,
                "errorMessage": self.Message,
                "httpCode": self.HTTPCode,
                "requestID": self.RequestID,
                "responseParameters": {
                    "migrate_to_chat_id": self.ResponseParameters.MigrateToChatID,
                    "retry_after": self.ResponseParameters.RetryAfter,
                },
            },
            ensure_ascii=False,
            indent=4,
        )


@dataclass
class User:
    UserId: str = ""
    IsBot: bool = False
    Name: str = ""
    Address: str = ""
    Pic: str = ""
    LanguageCode: str = ""

    def String(self) -> str:
        return self.Name or ""

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["User"]:
        if not isinstance(data, dict):
            return None
        return cls(
            UserId=str(data.get("user_id", "") or ""),
            IsBot=bool(data.get("is_bot", False)),
            Name=str(data.get("name", "") or ""),
            Address=str(data.get("address", "") or ""),
            Pic=str(data.get("pic", "") or ""),
            LanguageCode=str(data.get("language_code", "") or ""),
        )


@dataclass
class Chat:
    ID: str = ""
    Type: str = ""
    Title: str = ""
    UserName: str = ""
    FirstName: str = ""
    LastName: str = ""
    Bio: str = ""
    HasPrivateForwards: bool = False
    Description: str = ""
    InviteLink: str = ""
    PinnedMessage: Optional["Message"] = None
    SlowModeDelay: int = 0
    MessageAutoDeleteTime: int = 0
    HasProtectedContent: bool = False
    StickerSetName: str = ""
    CanSetStickerSet: bool = False
    LinkedChatID: int = 0

    def IsPrivate(self) -> bool:
        return self.Type == "private"

    def IsGroup(self) -> bool:
        return self.Type == "group"

    def IsSuperGroup(self) -> bool:
        return self.Type == "supergroup"

    def IsChannel(self) -> bool:
        return self.Type == "channel"

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["Chat"]:
        if not isinstance(data, dict):
            return None
        return cls(
            ID=str(data.get("id", "") or ""),
            Type=str(data.get("type", "") or ""),
            Title=str(data.get("title", "") or ""),
            UserName=str(data.get("username", "") or ""),
            FirstName=str(data.get("first_name", "") or ""),
            LastName=str(data.get("last_name", "") or ""),
            Bio=str(data.get("bio", "") or ""),
            HasPrivateForwards=bool(data.get("has_private_forwards", False)),
            Description=str(data.get("description", "") or ""),
            InviteLink=str(data.get("invite_link", "") or ""),
            SlowModeDelay=int(data.get("slow_mode_delay", 0) or 0),
            MessageAutoDeleteTime=int(data.get("message_auto_delete_time", 0) or 0),
            HasProtectedContent=bool(data.get("has_protected_content", False)),
            StickerSetName=str(data.get("sticker_set_name", "") or ""),
            CanSetStickerSet=bool(data.get("can_set_sticker_set", False)),
            LinkedChatID=int(data.get("linked_chat_id", 0) or 0),
        )


@dataclass
class MessageID:
    MessageID: int = 0


@dataclass
class Audio:
    FileID: str = ""
    FileUniqueID: str = ""
    Duration: int = 0
    Performer: str = ""
    Title: str = ""
    FileName: str = ""
    MimeType: str = ""
    FileSize: int = 0


@dataclass
class Video:
    FileID: str = ""
    FileUniqueID: str = ""
    Width: int = 0
    Height: int = 0
    Duration: int = 0
    FileName: str = ""
    MimeType: str = ""
    FileSize: int = 0


@dataclass
class KeyboardButtonPollType:
    Type: str = ""


@dataclass
class KeyboardButton:
    Text: str = ""
    RequestContact: bool = False
    RequestLocation: bool = False
    RequestPoll: Optional[KeyboardButtonPollType] = None


@dataclass
class ReplyKeyboardMarkup:
    Keyboard: List[List[KeyboardButton]] = field(default_factory=list)
    ResizeKeyboard: bool = False
    OneTimeKeyboard: bool = False
    InputFieldPlaceholder: str = ""
    Selective: bool = False


@dataclass
class ReplyKeyboardRemove:
    RemoveKeyboard: bool = True
    Selective: bool = False


@dataclass
class LoginURL:
    URL: str = ""
    ForwardText: str = ""
    BotUsername: str = ""
    RequestWriteAccess: bool = False


@dataclass
class InlineKeyboardButton:
    Text: str = ""
    URL: Optional[str] = None
    SubText: str = ""
    SubTextColor: str = ""
    LoginURL: Optional[LoginURL] = None
    CallbackData: Optional[str] = None
    SwitchInlineQuery: Optional[str] = None
    SwitchInlineQueryCurrentChat: Optional[str] = None
    Pay: bool = False


@dataclass
class InlineKeyboardMarkup:
    InlineKeyboard: List[List[InlineKeyboardButton]] = field(default_factory=list)
    FontSize: str = ""
    FontColor: str = ""


@dataclass
class ForceReply:
    ForceReply: bool = True
    InputFieldPlaceholder: str = ""
    Selective: bool = False


@dataclass
class BotCommand:
    Command: str = ""
    Description: str = ""


@dataclass
class BotCommandScope:
    Type: str = ""
    ChatID: int = 0
    UserID: int = 0


@dataclass
class UITagA:
    Uitag: str = ""
    Text: str = ""
    Href: str = ""


@dataclass
class UITagImg:
    Uitag: str = ""
    Src: str = ""
    Position: str = ""
    Height: str = ""
    Href: str = ""


@dataclass
class Message:
    MessageID: str = ""
    Text: str = ""
    TextRaw: str = ""
    MentionUsers: List[User] = field(default_factory=list)
    From: Optional[User] = None
    Chat: Optional[Chat] = None
    SenderChat: Optional[Chat] = None
    Date: int = 0
    ForwardFrom: Optional[User] = None
    ForwardFromChat: Optional[Chat] = None
    ForwardFromMessageID: int = 0
    ForwardSignature: str = ""
    ForwardSenderName: str = ""
    ForwardDate: int = 0
    IsAutomaticForward: bool = False
    ReplyToMessage: Optional["Message"] = None
    ViaBot: Optional[User] = None
    Caption: str = ""
    NewChatMembers: List[User] = field(default_factory=list)
    LeftChatMember: Optional[User] = None
    NewChatTitle: str = ""
    GroupChatCreated: bool = False
    SuperGroupChatCreated: bool = False
    ChannelChatCreated: bool = False
    MigrateToChatID: int = 0
    MigrateFromChatID: int = 0
    PinnedMessage: Optional["Message"] = None
    ConnectedWebsite: str = ""
    ReplyMarkup: Optional[InlineKeyboardMarkup] = None

    def Time(self) -> _dt.datetime:
        return _dt.datetime.fromtimestamp(self.Date, tz=_dt.timezone.utc)

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["Message"]:
        if not isinstance(data, dict):
            return None
        mention_users = [u for u in (User.from_dict(v) for v in data.get("mention_users", [])) if u]
        new_members = [u for u in (User.from_dict(v) for v in data.get("new_chat_members", [])) if u]
        reply_markup = data.get("reply_markup")
        parsed_reply_markup = None
        if isinstance(reply_markup, dict):
            parsed_reply_markup = _inline_markup_from_dict(reply_markup)

        return cls(
            MessageID=str(data.get("message_id", "") or ""),
            Text=str(data.get("text", "") or ""),
            TextRaw=str(data.get("text_raw", "") or ""),
            MentionUsers=mention_users,
            From=User.from_dict(data.get("from")),
            Chat=Chat.from_dict(data.get("chat")),
            SenderChat=Chat.from_dict(data.get("sender_chat")),
            Date=int(data.get("date", 0) or 0),
            ForwardFrom=User.from_dict(data.get("forward_from")),
            ForwardFromChat=Chat.from_dict(data.get("forward_from_chat")),
            ForwardFromMessageID=int(data.get("forward_from_message_id", 0) or 0),
            ForwardSignature=str(data.get("forward_signature", "") or ""),
            ForwardSenderName=str(data.get("forward_sender_name", "") or ""),
            ForwardDate=int(data.get("forward_date", 0) or 0),
            IsAutomaticForward=bool(data.get("is_automatic_forward", False)),
            ReplyToMessage=Message.from_dict(data.get("reply_to_message")),
            ViaBot=User.from_dict(data.get("via_bot")),
            Caption=str(data.get("caption", "") or ""),
            NewChatMembers=new_members,
            LeftChatMember=User.from_dict(data.get("left_chat_member")),
            NewChatTitle=str(data.get("new_chat_title", "") or ""),
            GroupChatCreated=bool(data.get("group_chat_created", False)),
            SuperGroupChatCreated=bool(data.get("supergroup_chat_created", False)),
            ChannelChatCreated=bool(data.get("channel_chat_created", False)),
            MigrateToChatID=int(data.get("migrate_to_chat_id", 0) or 0),
            MigrateFromChatID=int(data.get("migrate_from_chat_id", 0) or 0),
            PinnedMessage=Message.from_dict(data.get("pinned_message")),
            ConnectedWebsite=str(data.get("connected_website", "") or ""),
            ReplyMarkup=parsed_reply_markup,
        )


@dataclass
class CallbackQuery:
    ID: str = ""
    From: Optional[User] = None
    Message: Optional[Message] = None
    InlineMessageID: str = ""
    ChatInstance: str = ""
    Data: str = ""
    GameShortName: str = ""

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["CallbackQuery"]:
        if not isinstance(data, dict):
            return None
        return cls(
            ID=str(data.get("id", "") or ""),
            From=User.from_dict(data.get("from")),
            Message=Message.from_dict(data.get("message")),
            InlineMessageID=str(data.get("inline_message_id", "") or ""),
            ChatInstance=str(data.get("chat_instance", "") or ""),
            Data=str(data.get("data", "") or ""),
            GameShortName=str(data.get("game_short_name", "") or ""),
        )


@dataclass
class Update:
    Id: int = 0
    Message: Optional[Message] = None
    CallbackQuery: Optional[CallbackQuery] = None

    def SentFrom(self) -> Optional[User]:
        if self.Message is not None:
            return self.Message.From
        if self.CallbackQuery is not None:
            return self.CallbackQuery.From
        return None

    def CallbackData(self) -> str:
        if self.CallbackQuery is not None:
            return self.CallbackQuery.Data
        return ""

    def FromChat(self) -> Optional[Chat]:
        if self.Message is not None:
            return self.Message.Chat
        if self.CallbackQuery is not None and self.CallbackQuery.Message is not None:
            return self.CallbackQuery.Message.Chat
        return None

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["Update"]:
        if not isinstance(data, dict):
            return None
        return cls(
            Id=int(data.get("id", 0) or 0),
            Message=Message.from_dict(data.get("message")),
            CallbackQuery=CallbackQuery.from_dict(data.get("callback_query")),
        )


class UpdatesChannel(list):
    def Clear(self) -> None:
        self.clear()


def _inline_markup_from_dict(data: Dict[str, Any]) -> InlineKeyboardMarkup:
    rows: List[List[InlineKeyboardButton]] = []
    for row in data.get("inline_keyboard", []):
        btn_row: List[InlineKeyboardButton] = []
        for b in row:
            login_url = b.get("login_url") if isinstance(b, dict) else None
            parsed_login_url = None
            if isinstance(login_url, dict):
                parsed_login_url = LoginURL(
                    URL=str(login_url.get("url", "") or ""),
                    ForwardText=str(login_url.get("forward_text", "") or ""),
                    BotUsername=str(login_url.get("bot_username", "") or ""),
                    RequestWriteAccess=bool(login_url.get("request_write_access", False)),
                )
            btn_row.append(
                InlineKeyboardButton(
                    Text=str(b.get("text", "") or ""),
                    URL=b.get("url"),
                    SubText=str(b.get("sub_text", "") or ""),
                    SubTextColor=str(b.get("sub_text_color", "") or ""),
                    LoginURL=parsed_login_url,
                    CallbackData=b.get("callback_data"),
                    SwitchInlineQuery=b.get("switch_inline_query"),
                    SwitchInlineQueryCurrentChat=b.get("switch_inline_query_current_chat"),
                    Pay=bool(b.get("pay", False)),
                )
            )
        rows.append(btn_row)

    return InlineKeyboardMarkup(
        InlineKeyboard=rows,
        FontSize=str(data.get("font_size", "") or ""),
        FontColor=str(data.get("font_color", "") or ""),
    )
