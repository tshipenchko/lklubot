from typing import Any

from fastapi import FastAPI, Header
from aiogram import Bot, Dispatcher, types


def generate_app(bot: Bot, dp: Dispatcher, expected_secret: str) -> FastAPI:
    app = FastAPI()

    @app.post("/webhook")
    async def route_webhook(
            update: types.Update,
            secret: str = Header(alias="X-Telegram-Bot-Api-Secret-Token"),
    ) -> dict[str, Any]:
        if secret != expected_secret:
            return {"ok": False, "message": "Invalid secret token"}

        await dp.feed_update(bot=bot, update=update)
        return {"ok": True}

    return app
