from os import getenv

from dotenv import load_dotenv
from aiogram import Bot

if __name__ == '__main__':
    load_dotenv()

    bot = Bot(
        token=getenv("BOT_TOKEN"),
    )
    if await bot.set_webhook(
        url=getenv("WEBHOOK_URL"),
        secret_token=getenv("WEBHOOK_SECRET"),
    ):
        print("Webhook was set successfully")
    else:
        print("Webhook was not set")
