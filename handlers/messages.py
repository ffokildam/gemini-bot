from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from services import generate_gemini_flash_response, generate_gemini_pro_response
from utils import escape_markdown, chat_history, user_model_preference


router = Router()


@router.message()
async def handle_message(message: types.Message):
    user_message = message.text
    user_id = message.from_user.id


    if user_id not in user_model_preference:
        user_model_preference[user_id] = "gemini-1.5-flash"

    thinking_message = await message.reply(escape_markdown("Ожидание ответа от Gemini..."))

    if user_model_preference[user_id] == "gemini-1.5-flash":
        bot_reply = generate_gemini_flash_response(user_message, user_id, chat_history)
    else:
        bot_reply = generate_gemini_pro_response(user_message, user_id, chat_history)

    await thinking_message.delete()


    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Очистить историю чата", callback_data="clear_history")],
            [InlineKeyboardButton(
                text=escape_markdown(f"Переключить на {'Pro' if user_model_preference[user_id] == 'gemini-1.5-flash' else 'Flash'}"),
                callback_data="switch_model"
            )]
        ]
    )

    await message.reply(
        escape_markdown(bot_reply),
        parse_mode="MarkdownV2",
        reply_markup=keyboard
    )
