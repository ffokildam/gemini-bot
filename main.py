import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
import re
import logging
import asyncio
import os

logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

dp = Dispatcher()

chat_history = {}

def escape_markdown(text):
    text = re.sub(r'(?<!\*)\*(?!\*)', r'\\*', text)  
    return re.sub(r'([_\[\]()~>#+\-=|{}.!])', r'\\\1', text)

def generate_response(user_message, user_id):
    if user_id not in chat_history:
        chat_history[user_id] = [
        ]
    
    chat_history[user_id].append({"role": "user", "parts": user_message})
    

    if len(chat_history[user_id]) > 40:
        chat_history[user_id] = chat_history[user_id][1:]
    

    chat = model.start_chat(history=chat_history[user_id])
    response = chat.send_message(user_message)
    

    chat_history[user_id].append({"role": "model", "parts": response.text})

    return response.text


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.reply(escape_markdown("Я бот, работающий с Gemini1.5 Flash. Как я могу помочь?"))

@dp.message()
async def handle_message(message: types.Message):
    user_message = message.text
    user_id = message.from_user.id


    thinking_message = await message.reply(escape_markdown("Ожидание ответа от Gemini..."))

    bot_reply = generate_response(user_message, user_id)

    print(user_message)
    print(bot_reply)

    await thinking_message.delete()


    await message.reply(escape_markdown(bot_reply), parse_mode="MarkdownV2")

async def main() -> None:
    bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode="MarkdownV2"))
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
