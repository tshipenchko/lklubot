from abc import ABC
from typing import Any, Union

from aiogram import Bot, types
from aiogram.filters import Filter


class IsChatAdmin(Filter, ABC):
    async def __call__(self, event: Union[types.Message, types.CallbackQuery], bot: Bot) -> bool:
        member = await bot.get_chat_member(event.chat.id, event.from_user.id)
        return isinstance(member, types.ChatMemberAdministrator)


class CanPromoteMembers(Filter, ABC):
    async def __call__(self, event: Union[types.Message, types.CallbackQuery], bot: Bot) -> bool:
        member = await bot.get_chat_member(event.chat.id, event.from_user.id)
        return (
                isinstance(member, types.ChatMemberAdministrator)
                and member.can_promote_members
                or isinstance(member, types.ChatMemberOwner)
        )


class ReplyRequired(Filter, ABC):
    def __init__(self, error_message: str = "Reply to message is required", notify: bool = True):
        self.error_message = error_message
        self.notify = notify

    async def __call__(self, event: types.Message, bot: Bot) -> Union[bool, dict[str, Any]]:
        if event.reply_to_message:
            return {
                "reply": event.reply_to_message,
            }

        if self.notify:
            await event.answer(self.error_message)
        return False
