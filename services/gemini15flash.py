import google.generativeai as genai
from config import GEMINI_API_KEY
from utils import token_counts_flash
from config import WHITELIST_USER_IDS

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_gemini_flash_response(user_message, user_id, chat_history):
    if user_id not in chat_history:
        chat_history[user_id] = []

    if user_id not in token_counts_flash:
        token_counts_flash[user_id] = 0

    if user_id not in WHITELIST_USER_IDS and token_counts_flash[user_id] >= 25000:
        return "Ваш лимит токен для Gemini Flash израсходован.\nЛимит сбрасывается каждые сутки в 12:00 по МСК."

    chat_history[user_id].append({"role": "user", "parts": user_message})

    if len(chat_history[user_id]) > 40:
        chat_history[user_id] = chat_history[user_id][1:]

    chat = model.start_chat(history=chat_history[user_id])
    response = chat.send_message(user_message)

    total_tokens = int(response.usage_metadata.total_token_count)
    token_counts_flash[user_id] += total_tokens

    chat_history[user_id].append({"role": "model", "parts": response.text})

    return response.text
