from __future__ import annotations

import logging
import os

import boxbotapi
from boxbotapi import configs as cfg

homeInfoContent = """<body href="%s"><b>Bot首页</b> <br/> 我是Debox官方演示机器人，展示Bot部分能力，供开发者参考。<br/>
					1、可以通过发送<b>botmother</b>消息直接唤醒我<br/>
					2、可以点击<a href="%s">@botmother</a>进入私聊交互。<br/>
					3、该Bot代码很少共218行，去掉注释后<font color="#0000ff">源码只有196行</font>，演示了以下功能：<br/>
					• 消息监听<br/>
					• 消息发送<br/>
					• 消息编辑<br/>
					• 按钮传参<br/>
					• 静默授权<br/>
					• 充话费业务交互等功能<br/>• 同时演示了用HTML构造原生消息的能力，极大丰富了富文本承载信息的能力。<br/>
					4、您可以<a href="https://docs.debox.pro/zh/GO-SDK">下载源码</a>，基于源码开发自己的Bot服务。<br/>
					基于SDK和此Demo，开发Bot的难度和成本很低，您可以轻松搭建自己的Bot服务。
					<br/>点击下面按钮体验吧。</body>
					"""

homeButton = "首页"
myButton = "我是谁"
yourButton = "你是谁"
privateChatUrl = "https://m.debox.pro/user/chat?id="
userHomePage = "https://m.debox.pro/card?id="

homeMenuMarkup = boxbotapi.NewInlineKeyboardMarkup(
    boxbotapi.NewInlineKeyboardRow(
        boxbotapi.NewInlineKeyboardButtonDataWithColor("", yourButton, "", yourButton, "#21C161"),
        boxbotapi.NewInlineKeyboardButtonDataWithColor("", myButton, "", myButton, "#21C161"),
    ),
    boxbotapi.NewInlineKeyboardRow(
        boxbotapi.NewInlineKeyboardButtonData(homeButton, homeButton),
    ),
)

cardSample = """
<body href="%s">
	<div style="background-color1:#00ff00;width:80%%;color:#8a8a8a">
		<img src="%s" style="width:10%%;height:10%%;vertical-align:middle;border-radius: 50%%;radius:-1"/>%s
	</div>
		<b>Address: </b>%s
		<br/>
		<img src="%s" style="width:100%%;height:100%%;"/>
	<div style="width:70%%">
		<font style="font-size:12px;color:#8a8a8a">🏠</font>
		<font style="font-size:12px;color:#8a8a8a">%s</font>
	</div>
</body>
"""

bot: boxbotapi.BotAPI


def setSelected(keyboard: boxbotapi.InlineKeyboardMarkup, row: int, col: int) -> None:
    for i in range(len(keyboard.InlineKeyboard[row])):
        keyboard.InlineKeyboard[row][i].SubTextColor = "#21C161"
        if col == i:
            keyboard.InlineKeyboard[row][i].SubTextColor = "#ff0000"


def handleMessage(message: boxbotapi.Message) -> None:
    user = message.From
    text = message.Text

    if user is None:
        return

    logging.info("%s wrote %s", user.Name, text)

    if len(text) > 0:
        msg = boxbotapi.NewMessage(message.Chat.ID, message.Chat.Type, message.Text)
        msg.ParseMode = boxbotapi.ModeHTML

        if text.lower() == "botmother" or message.Chat.Type == "private":
            msg.Text = homeInfoContent % (privateChatUrl + bot.Self.UserId, privateChatUrl + bot.Self.UserId)
            setSelected(homeMenuMarkup, 0, 100)
            msg.ReplyMarkup = homeMenuMarkup
            bot.Send(msg)


def handleButton(query: boxbotapi.CallbackQuery) -> None:
    text = ""
    message = query.Message

    markup = boxbotapi.NewInlineKeyboardMarkup()
    if query.Data == homeButton:
        user = bot.Self
        homePage = userHomePage + user.UserId
        text = homeInfoContent % (homePage, privateChatUrl + user.UserId)
        setSelected(homeMenuMarkup, 0, 100)
        markup = homeMenuMarkup
    elif query.Data == yourButton:
        user = bot.Self
        homePage = userHomePage + user.UserId
        text = cardSample % (homePage, user.Pic, user.Name, user.Address, user.Pic, homePage)
        markup = homeMenuMarkup
        setSelected(homeMenuMarkup, 0, 0)
    elif query.Data == myButton:
        user = query.From
        homePage = userHomePage + user.UserId
        text = cardSample % (homePage, user.Pic, user.Name, user.Address, user.Pic, homePage)
        markup = homeMenuMarkup
        setSelected(homeMenuMarkup, 0, 1)

    msg = boxbotapi.NewEditMessageTextAndMarkup(message.Chat.ID, message.Chat.Type, message.MessageID, text, markup)
    msg.ParseMode = boxbotapi.ModeHTML
    bot.Send(msg)


def handleUpdate(update: boxbotapi.Update) -> None:
    if update.Message is not None:
        handleMessage(update.Message)
    elif update.CallbackQuery is not None:
        handleButton(update.CallbackQuery)


def receiveUpdates(updates: boxbotapi.UpdatesChannel) -> None:
    for update in updates:
        handleUpdate(update)


def main() -> None:
    global bot

    # token = os.getenv("DEBOX_BOT_API_KEY", "YOUR_BOT_API_KEY")
    token = "9tAwKmXodvMs9zdLR9xAmGTxbN09";

    api_secret = os.getenv("DEBOX_BOT_API_SECRET", "")

    cfg.Debug = True
    cfg.MessageListener = True

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logging.info(
        "application started, debug mode is %s, message listener is %s",
        cfg.Debug,
        cfg.MessageListener,
    )

    bot = boxbotapi.NewBotAPI(token, api_secret)

    u = boxbotapi.NewUpdate(0)
    u.Timeout = 60

    updates = bot.GetUpdatesChan(u)
    receiveUpdates(updates)


if __name__ == "__main__":
    main()
