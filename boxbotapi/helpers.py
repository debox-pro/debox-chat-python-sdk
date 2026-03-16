from __future__ import annotations

from .configs import (
    BaseChat,
    BaseEdit,
    CallbackConfig,
    EditMessageTextConfig,
    MessageConfig,
    MessageToFansConfig,
    UpdateConfig,
)
from .types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    LoginURL,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)


def NewMessage(chatID: str, chatType: str, text: str) -> MessageConfig:
    return MessageConfig(BaseChat=BaseChat(ChatID=chatID, ChatType=chatType), Text=text)


def NewMessageResponse(message: Message) -> MessageConfig:
    chat_id = message.Chat.ID if message.Chat else ""
    chat_type = message.Chat.Type if message.Chat else ""
    return MessageConfig(BaseChat=BaseChat(ChatID=chat_id, ChatType=chat_type), Text=message.Text)


def NewMessageToFans(chatID: str, chatType: str, text: str) -> MessageToFansConfig:
    return MessageToFansConfig(BaseChat=BaseChat(ChatID=chatID, ChatType=chatType), Text=text)


def NewEditMessageText(chatID: str, chatType: str, messageID: str, text: str) -> EditMessageTextConfig:
    return EditMessageTextConfig(
        BaseEdit=BaseEdit(ChatID=chatID, ChatType=chatType, MessageID=messageID),
        Text=text,
    )


def NewEditMessageTextAndMarkup(
    chatID: str, chatType: str, messageID: str, text: str, replyMarkup: InlineKeyboardMarkup
) -> EditMessageTextConfig:
    return EditMessageTextConfig(
        BaseEdit=BaseEdit(
            ChatID=chatID,
            ChatType=chatType,
            MessageID=messageID,
            ReplyMarkup=replyMarkup,
        ),
        Text=text,
    )


def NewMessageToChannel(username: str, text: str) -> MessageConfig:
    return MessageConfig(BaseChat=BaseChat(ChannelUsername=username), Text=text)


def NewUpdate(offset: int) -> UpdateConfig:
    return UpdateConfig(Offset=offset, Limit=0, Timeout=0)


def NewRemoveKeyboard(selective: bool) -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove(RemoveKeyboard=True, Selective=selective)


def NewKeyboardButton(text: str) -> KeyboardButton:
    return KeyboardButton(Text=text)


def NewKeyboardButtonContact(text: str) -> KeyboardButton:
    return KeyboardButton(Text=text, RequestContact=True)


def NewKeyboardButtonLocation(text: str) -> KeyboardButton:
    return KeyboardButton(Text=text, RequestLocation=True)


def NewKeyboardButtonRow(*buttons: KeyboardButton) -> list[KeyboardButton]:
    return list(buttons)


def NewReplyKeyboard(*rows: list[KeyboardButton]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(ResizeKeyboard=True, Keyboard=list(rows))


def NewOneTimeReplyKeyboard(*rows: list[KeyboardButton]) -> ReplyKeyboardMarkup:
    markup = NewReplyKeyboard(*rows)
    markup.OneTimeKeyboard = True
    return markup


def NewInlineKeyboardButtonData(text: str, data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(Text=text, CallbackData=data)


def NewInlineKeyboardButtonDataWithColor(
    text: str, data: str, url: str, subText: str, subTextColor: str
) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        Text=text,
        CallbackData=data,
        URL=url,
        SubText=subText,
        SubTextColor=subTextColor,
    )


def NewInlineKeyboardButtonLoginURL(text: str, loginURL: LoginURL) -> InlineKeyboardButton:
    return InlineKeyboardButton(Text=text, LoginURL=loginURL)


def NewInlineKeyboardButtonURL(text: str, url: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(Text=text, URL=url)


def NewInlineKeyboardButtonSwitch(text: str, sw: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(Text=text, SwitchInlineQuery=sw)


def NewInlineKeyboardRow(*buttons: InlineKeyboardButton) -> list[InlineKeyboardButton]:
    return list(buttons)


def NewInlineKeyboardMarkup(*rows: list[InlineKeyboardButton]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(InlineKeyboard=list(rows))


def NewCallback(id: str, text: str) -> CallbackConfig:
    return CallbackConfig(CallbackQueryID=id, Text=text, ShowAlert=False)


def NewCallbackWithAlert(id: str, text: str) -> CallbackConfig:
    return CallbackConfig(CallbackQueryID=id, Text=text, ShowAlert=True)
