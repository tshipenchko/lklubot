from aiogram import Router, types, Bot
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types.error_event import ErrorEvent

from filters import IsChatAdmin, CanPromoteMembers, ReplyRequired

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.reply("Standard start message")


@router.message(Command("help"))
async def cmd_help(message: types.Message) -> None:
    await message.reply(
        "Commands:\n"
        "/promote [reply] - promote user to admin\n"
        "/demote [reply] - demote user from admin\n"
        "/nick [text] - change custom admin title\n"
        "  * available only for admins\n"
        "/nick [reply] [text] - change custom admin title\n"
        "  * available only for admins who can promote members\n"
    )


@router.message(Command("promote"), CanPromoteMembers(), ReplyRequired())
async def cmd_promote(message: types.Message, bot: Bot, command: CommandObject, reply: types.Message) -> None:
    user = reply.from_user
    await bot.promote_chat_member(
        message.chat.id,
        user.id,
        can_invite_users=True,
    )

    if command.args:
        await bot.set_chat_administrator_custom_title(message.chat.id, user.id, command.args)

    await message.reply(f"User {user.full_name} promoted to admin")


@router.message(Command("demote"), CanPromoteMembers(), ReplyRequired())
async def cmd_demote(message: types.Message, bot: Bot, reply: types.Message) -> None:
    user = reply.from_user

    # Kinda ugly, but aiogram-dev currently hasn't implementation of Bot.demote_chat_member(...)
    await bot.promote_chat_member(
        message.chat.id,
        user.id,
        is_anonymous=False,
        can_manage_chat=False,
        can_post_messages=False,
        can_edit_messages=False,
        can_delete_messages=False,
        can_manage_video_chats=False,
        can_restrict_members=False,
        can_promote_members=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False,
        can_manage_topics=False,
    )
    await message.reply(f"User {user.full_name} demoted from admin")


@router.message(
    Command("nick"),
    CanPromoteMembers(),
    ReplyRequired(notify=False, error_message="Reply to user to change his title")
)
async def cmd_nick(message: types.Message, bot: Bot, command: CommandObject, reply: types.Message) -> None:
    await bot.set_chat_administrator_custom_title(
        message.chat.id,
        reply.from_user.id,
        command.args,
    )
    await message.reply(f"User {reply.from_user.full_name} title changed to {command.args}")


@router.message(Command("nick"), IsChatAdmin())
async def cmd_nick(message: types.Message, bot: Bot, command: CommandObject) -> None:
    user = message.from_user
    await bot.set_chat_administrator_custom_title(
        message.chat.id,
        user.id,
        command.args,
    )
    await message.reply(f"User {user.full_name} custom admin title changed")


@router.message(Command("nick"))
async def cmd_nick(message: types.Message) -> None:
    await message.reply("You must be admin to change your title")


@router.errors()
async def errors_handler(error: ErrorEvent) -> None:
    event = getattr(error.update, error.update.event_type)
    text = f"Error: \n{error.exception}"
    if len(text) > 200:
        text = f"{text[:200]}..."
    if isinstance(event, types.Message):
        await event.reply(text)
    elif isinstance(event, types.CallbackQuery):
        await event.answer(text)
