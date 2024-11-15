import google.generativeai as genai
from config import GEMINI_API_KEY, WHITELIST_USER_IDS
import requests
from PIL import Image
from io import BytesIO
from utils import token_counts_pro


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_gemini_pro_response(user_message, user_id, chat_history, imageUrl=None):
    if user_id not in chat_history or chat_history[user_id] is None:
        chat_history[user_id] = []

    if user_id not in token_counts_pro:
        token_counts_pro[user_id] = 0

    if user_id not in WHITELIST_USER_IDS and token_counts_pro[user_id] >= 5000:
        return "Ваш лимит токен для Gemini Pro израсходован.\nЛимит сбрасывается каждые сутки в 12:00 по МСК."

    if user_message:
        chat_history[user_id].append({"role": "user", "parts": user_message})

    # Trim chat history if too long
    if len(chat_history[user_id]) > 30:
        chat_history[user_id] = chat_history[user_id][1:]

    if imageUrl:
        response = requests.get(imageUrl).content
        img = Image.open(BytesIO(response))
        prompt = str(user_message)

        print(f"Image type: {type(img)}")

        response = model.generate_content([img, prompt])
        response_text = response.text
        chat_history[user_id].append({"role": "model", "parts": response_text})

    else:
        chat = model.start_chat(history=chat_history[user_id])
        response = chat.send_message(user_message)
        chat_history[user_id].append({"role": "model", "parts": response.text})
        response_text = response.text

    total_tokens = int(response.usage_metadata.total_token_count)
    token_counts_pro[user_id] += total_tokens

    print(token_counts_pro[user_id])
    return response_text
