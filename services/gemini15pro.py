import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")

def generate_gemini_pro_response(user_message, user_id, chat_history):
    if user_id not in chat_history:
        chat_history[user_id] = []

    chat_history[user_id].append({"role": "user", "parts": user_message})

    if len(chat_history[user_id]) > 30:
        chat_history[user_id] = chat_history[user_id][1:]

    chat = model.start_chat(history=chat_history[user_id])
    response = chat.send_message(user_message)

    chat_history[user_id].append({"role": "model", "parts": response.text})
    print("used pro")
    return response.text
