import unittest

import boxbotapi


class TestHelpers(unittest.TestCase):
    def test_new_inline_keyboard_button_login_url(self) -> None:
        result = boxbotapi.NewInlineKeyboardButtonLoginURL(
            "text",
            boxbotapi.LoginURL(
                URL="url",
                ForwardText="ForwardText",
                BotUsername="username",
                RequestWriteAccess=False,
            ),
        )

        self.assertEqual("text", result.Text)
        self.assertIsNotNone(result.LoginURL)
        self.assertEqual("url", result.LoginURL.URL)
        self.assertEqual("ForwardText", result.LoginURL.ForwardText)
        self.assertEqual("username", result.LoginURL.BotUsername)
        self.assertFalse(result.LoginURL.RequestWriteAccess)

    def test_new_message_and_keyboard_helpers(self) -> None:
        msg = boxbotapi.NewMessage("chat_1", "group", "hello")
        row = boxbotapi.NewInlineKeyboardRow(
            boxbotapi.NewInlineKeyboardButtonData("next", "next")
        )
        msg.ReplyMarkup = boxbotapi.NewInlineKeyboardMarkup(row)

        self.assertEqual("chat_1", msg.ChatID)
        self.assertEqual("group", msg.ChatType)
        self.assertEqual("bot/sendMessage", msg.method())
        self.assertIsNotNone(msg.ReplyMarkup)


if __name__ == "__main__":
    unittest.main()
