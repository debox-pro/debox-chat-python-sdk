import datetime as dt
import unittest

import boxbotapi


class TestTypes(unittest.TestCase):
    def test_user_string(self) -> None:
        user = boxbotapi.User(UserId="u1", Name="@test")
        self.assertEqual("@test", user.String())

        user2 = boxbotapi.User(UserId="u2", Name="")
        self.assertEqual("", user2.String())

    def test_message_time(self) -> None:
        message = boxbotapi.Message(Date=0)
        self.assertEqual(dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc), message.Time())

    def test_chat_type_helpers(self) -> None:
        self.assertTrue(boxbotapi.Chat(ID="c1", Type="private").IsPrivate())
        self.assertTrue(boxbotapi.Chat(ID="c1", Type="group").IsGroup())
        self.assertTrue(boxbotapi.Chat(ID="c1", Type="channel").IsChannel())
        self.assertTrue(boxbotapi.Chat(ID="c1", Type="supergroup").IsSuperGroup())

    def test_update_helpers(self) -> None:
        update = boxbotapi.Update(
            Id=1,
            Message=boxbotapi.Message(
                Text="hello",
                From=boxbotapi.User(UserId="u1", Name="alice"),
                Chat=boxbotapi.Chat(ID="chat_1", Type="private"),
            ),
        )
        self.assertEqual("alice", update.SentFrom().Name)
        self.assertEqual("chat_1", update.FromChat().ID)
        self.assertEqual("", update.CallbackData())


if __name__ == "__main__":
    unittest.main()
