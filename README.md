# debox-chat-python-sdk

`debox-chat-python-sdk` is the official Python SDK for the DeBox Chat Service.

[Chinese version](./README_CN.md)

## Quick Start

```bash
pip install -e .
```

```python
import boxbotapi

bot = boxbotapi.NewBotAPI("YOUR_BOT_API_KEY")
msg = boxbotapi.NewMessage("DEBOX_USER_ID", "private", "Hello, DeBox!")
bot.Send(msg)
```

## Documentation

See [DeBox docs](https://docs.debox.pro/GO-SDK/) and API guides at [developer.debox.pro](https://developer.debox.pro/).
