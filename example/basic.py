import boxbotapi


def main() -> None:
    bot = boxbotapi.NewBotAPI("YOUR_BOT_API_KEY", "YOUR_BOT_API_SECRET")
    msg = boxbotapi.NewMessage("DEBOX_USER_ID", "private", "Hello, DeBox!")
    bot.Send(msg)


if __name__ == "__main__":
    main()
