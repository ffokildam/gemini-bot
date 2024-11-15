from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
import asyncio
from config import TELEGRAM_TOKEN
from handlers import commands, messages, callbacks
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode="MarkdownV2"))
    dp = Dispatcher()
    
    dp.include_router(commands.router)
    dp.include_router(messages.router)
    dp.include_router(callbacks.router)
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
