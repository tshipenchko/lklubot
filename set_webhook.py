import asyncio
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot


async def set_webhook(bot: Bot, webhook_url, webhook_secret: str) -> None:
    if await bot.set_webhook(
            url=webhook_url,
            secret_token=webhook_secret,
    ):
        print("Webhook was set successfully")
    else:
        print("Webhook was not set")


async def main():
    load_dotenv()
    bot = Bot(
        token=getenv("BOT_TOKEN"),
    )
    try:
        await set_webhook(
            bot,
            getenv("WEBHOOK_URL"),
            getenv("WEBHOOK_SECRET"),
        )
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
