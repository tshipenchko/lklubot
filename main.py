import logging
from os import getenv

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers import router


load_dotenv()
bot = Bot(token=getenv("BOT_TOKEN"))
dp = Dispatcher()
dp.include_router(router)

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    dp.run_polling(bot)
