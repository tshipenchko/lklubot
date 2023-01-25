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


if getenv("DETA_RUNTIME"):
    from deta_shit import generate_app
    app = generate_app(
        bot,
        dp,
        getenv("WEBHOOK_SECRET"),
    )
else:
    dp.run_polling(bot)
