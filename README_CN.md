# debox-chat-python-sdk

`debox-chat-python-sdk` 是 DeBox Chat Service 的官方 Python SDK。

[English](./README.md)

## 环境要求

- Python >= 3.9

## 工程入口

- SDK 包入口：`boxbotapi/`
- 可直接运行 Demo 入口：`main.py`

## 安装

```bash
pip install -e .
```

## 环境变量

```bash
export DEBOX_BOT_API_KEY="YOUR_BOT_API_KEY"
export DEBOX_BOT_API_SECRET="YOUR_BOT_API_SECRET"
```

## 快速用法

```python
import boxbotapi

bot = boxbotapi.NewBotAPI(
    "YOUR_BOT_API_KEY",
    "YOUR_BOT_API_SECRET",
)

msg = boxbotapi.NewMessage("DEBOX_USER_ID", "private", "你好，DeBox!")
bot.Send(msg)
```

## 运行 Demo（与 Go `main.go` 同流程复刻）

```bash
python3 main.py
```

Demo 默认流程：

- 启动时调用 `bot/getMe`
- 长轮询 `bot/getUpdates`
- 处理消息与按钮回调
- 通过 `bot/editMessageText` 编辑消息+按钮状态

## 最小监听示例

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
        msg = boxbotapi.NewMessage(update.Message.Chat.ID, update.Message.Chat.Type, "收到")
        bot.Send(msg)
```

## 签名说明

- 请求头包含：`X-API-KEY`、`nonce`、`timestamp`、`signature`、`X-Request-Id`
- 签名规则：`signature = sha1(apiSecret + nonce + timestamp)`

## 文档

- [DeBox 文档](https://docs.debox.pro/GO-SDK/)
- [开放平台](https://developer.debox.pro/)
