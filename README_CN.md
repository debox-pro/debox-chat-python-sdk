# debox-chat-python-sdk

`debox-chat-python-sdk` 是 DeBox 聊天服务的官方 Python SDK。

[English version](./README.md)

## 快速开始

```bash
pip install -e .
```

```python
import boxbotapi

bot = boxbotapi.NewBotAPI("YOUR_BOT_API_KEY")
msg = boxbotapi.NewMessage("DEBOX_USER_ID", "private", "Hello, DeBox!")
bot.Send(msg)
```

## 文档

可参考 [DeBox 文档](https://docs.debox.pro/GO-SDK/) 与 [开放平台](https://developer.debox.pro/)。
