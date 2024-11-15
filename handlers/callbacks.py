from aiogram import Router, types
from utils import escape_markdown, chat_history, user_model_preference, token_counts_pro, token_counts_flash


router = Router()


@router.callback_query()
async def handle_callback_query(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    if callback_query.data == "clear_history":

        if user_id in chat_history:
            del chat_history[user_id]
        await callback_query.message.answer(escape_markdown("История чата была успешно очищена."))
        await callback_query.answer()

    elif callback_query.data == "switch_model":

        if user_id in user_model_preference:
            current_model = user_model_preference[user_id]
            new_model = "gemini-1.5-pro" if current_model == "gemini-1.5-flash" else "gemini-1.5-flash"
            user_model_preference[user_id] = new_model

            await callback_query.message.answer(
                escape_markdown(f"Модель переключена на {new_model.replace('gemini-1.5-', '').capitalize()}.")
            )
        else:

            user_model_preference[user_id] = "gemini-1.5-flash"
            await callback_query.message.answer(escape_markdown("Модель переключена на Flash."))

        await callback_query.answer()

    elif callback_query.data == "look_up_tokens":
        response = ""
        if user_id in token_counts_pro:
            response += f"Ваши лимиты по Gemini Pro: {token_counts_pro[user_id]}/5000"
        if user_id in token_counts_flash:
            response += f"\nВаши лимиты по Gemini Flash: {token_counts_flash[user_id]}/25000"
        await callback_query.message.answer(escape_markdown(response))
        await callback_query.answer()

