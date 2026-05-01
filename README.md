# debox-chat-python-sdk

`debox-chat-python-sdk` is the official Python SDK for DeBox Chat Service.

[中文文档](./README_CN.md)

## Requirements

- Python >= 3.9

## Project Entry

- SDK package: `boxbotapi/`
- Runnable demo entry: `main.py`

## Install

```bash
pip install -e .
```

## Environment Variables

```bash
export DEBOX_BOT_API_KEY="YOUR_BOT_API_KEY"
export DEBOX_BOT_API_SECRET="YOUR_BOT_API_SECRET"
```

## Quick Usage

```python
import boxbotapi

bot = boxbotapi.NewBotAPI(
    "YOUR_BOT_API_KEY",
    "YOUR_BOT_API_SECRET",
)

msg = boxbotapi.NewMessage("DEBOX_USER_ID", "private", "Hello, DeBox!")
bot.Send(msg)
```

## Run Demo (1:1 with Go main.go flow)

```bash
python3 main.py
```

Demo behavior:

- Calls `bot/getMe` during startup
- Long-polls `bot/getUpdates`
- Handles text messages and callback buttons
- Edits message content with inline keyboard (`bot/editMessageText`)

## Minimal Bot Loop Example

```python
import boxbotapi
from boxbotapi import configs as cfg

cfg.Debug = False
cfg.MessageListener = True

bot = boxbotapi.NewBotAPI(
    "YOUR_BOT_API_KEY",
    "YOUR_BOT_API_SECRET",
)

u = boxbotapi.NewUpdate(0)
u.Timeout = 60

for update in bot.GetUpdatesChan(u):
    if update.Message is not None:
        msg = boxbotapi.NewMessage(update.Message.Chat.ID, update.Message.Chat.Type, "Received")
        bot.Send(msg)
```

## API Signature Notes

- Auth headers include `X-API-KEY`, `nonce`, `timestamp`, `signature`, `X-Request-Id`
- `signature = sha1(apiSecret + nonce + timestamp)`

## Documentation

- [DeBox docs](https://docs.debox.pro/GO-SDK/)
- [developer.debox.pro](https://developer.debox.pro/)
