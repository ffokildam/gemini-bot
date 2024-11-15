from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from services import generate_gemini_flash_response, generate_gemini_pro_response
from utils import escape_markdown, chat_history, user_model_preference
from main import logger
from config import TELEGRAM_TOKEN

router = Router()

@router.message()
async def handle_message(message: types.Message):
    user_message = message.text
    user_id = message.from_user.id
    username = message.from_user.full_name
    image_url = None


    if user_id not in user_model_preference:
        user_model_preference[user_id] = "gemini-1.5-flash"

    logger.info(f"User {username} (ID: {user_id})(MODEL:{user_model_preference[user_id]}) inputted prompt: {message.text}")

    thinking_message = await message.reply(escape_markdown("Ожидание ответа от Gemini..."))

    image = None
    if message.photo:
        file_id = message.photo[-1].file_id
        file = await message.bot.get_file(file_id)
        file_path = file.file_path
        image_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
        print(image_url)


    if user_model_preference[user_id] == "gemini-1.5-flash":
        if message.photo:
            bot_reply = escape_markdown("Flash ne ymeet v kartinki, usai PRO")
        else:
            bot_reply = generate_gemini_flash_response(user_message, user_id, chat_history)
    else:
        bot_reply = generate_gemini_pro_response(user_message, user_id, chat_history, imageUrl=image_url)

    logger.info(f"User {username} (ID: {user_id})(MODEL:{user_model_preference[user_id]}) received answer: {bot_reply}")

    await thinking_message.delete()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Очистить историю чата", callback_data="clear_history")],
            [InlineKeyboardButton(
                text=escape_markdown(f"Переключить на {'Pro' if user_model_preference[user_id] == 'gemini-1.5-flash' else 'Flash'}"),
                callback_data="switch_model"
            )],
            [InlineKeyboardButton(text="Просмотреть мои лимиты токенов",callback_data="look_up_tokens")],
        ]
    )

    await message.reply(

        escape_markdown(bot_reply),
        parse_mode="MarkdownV2",
        reply_markup=keyboard
    )
