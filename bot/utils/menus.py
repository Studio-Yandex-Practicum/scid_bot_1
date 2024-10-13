from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot, user_id: int):
    commands = [
        BotCommand(command='start', description='Начать'),
        BotCommand(command='review', description='Оставить отзыв'),
    ]
    # await bot.delete_my_commands()
    await bot.set_my_commands(commands, BotCommandScopeDefault())