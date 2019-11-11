import telepot
from django.conf import settings

telegramBot = telepot.Bot(settings.BOT_TOKEN)


def send_message(text):
    telegramBot.sendMessage(settings.CHAT_ID, text, parse_mode="Markdown")


def send_me_message(text):
    telegramBot.sendMessage(settings.ADMIN_ID, text, parse_mode="Markdown")
