from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Начать'),
        BotCommand(command='review', description='Оставить отзыв'),
        BotCommand(command='manager', description='Я менеджер'),
        BotCommand(command='admin', description='Я администратор'),
    ]
    await bot.delete_my_commands()
    await bot.set_my_commands(commands, BotCommandScopeDefault())