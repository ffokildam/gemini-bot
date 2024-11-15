from aiogram import Router, types
from aiogram.filters import CommandStart
from utils import escape_markdown

router = Router()

@router.message(CommandStart())
async def start_command(message: types.Message):
    await message.reply(escape_markdown("Я бот, работающий с Gemini1.5 Flash. Как я могу помочь?"))
