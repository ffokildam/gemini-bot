from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
import requests
import logging
import asyncio
import re
import os

logging.basicConfig(level=logging.INFO)


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=" + GEMINI_API_KEY

dp = Dispatcher()

def escape_markdown(text):
    # escape markdown symbols that are critical for tg markdown
    text = re.sub(r'(?<!\*)\*(?!\*)', r'\\*', text)  
    return re.sub(r'([_\[\]()~>#+\-=|{}.!])', r'\\\1', text)


def generate_response(user_message):
    payload = {
        "contents": [{"parts": [{"text": user_message}]}]
    }

    # sending request to gemini api

    response = requests.post(GEMINI_API_URL, json=payload)

    if response.status_code == 200:
        gemini_reply = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return gemini_reply
    else:
        return "Не удается получить ответ от Gemini, попробуйте позже."


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.reply(escape_markdown("Я бот, работающий с Gemini1.5 Flash. Как я могу помочь?"))


@dp.message()
async def handle_message(message: types.Message):
    user_message = message.text


    thinking_message = await message.reply(escape_markdown("Ожидание ответа от Gemini..."))

    bot_reply = generate_response(user_message)

    print(bot_reply)
    print(escape_markdown(bot_reply))

 
    await thinking_message.delete()

    await message.reply(escape_markdown(bot_reply), parse_mode="MarkdownV2")


async def main() -> None:
    bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode="MarkdownV2"))
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
