import google.generativeai as genai
from config import GEMINI_API_KEY
from main import logger
import requests
# from IPython.display import Image as DisplayImage
# from IPython.core.display import Image as CoreImage
# import os
from PIL import Image

from io import BytesIO


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_gemini_pro_response(user_message, user_id, chat_history, imageUrl=None):
    if user_id not in chat_history or chat_history[user_id] is None:
        chat_history[user_id] = []

    if user_message:
        chat_history[user_id].append({"role": "user", "parts": user_message})

    # Trim chat history if too long
    if len(chat_history[user_id]) > 30:
        chat_history[user_id] = chat_history[user_id][1:]

    if imageUrl:
        response = requests.get(imageUrl).content
        # img_path = f"{user_id}.png"
        # with open(img_path, 'wb') as f:
        #     f.write(response)
        #
        # img = DisplayImage(img_path)
        # print("Image true")
        img = Image.open(BytesIO(response))
        prompt = str(user_message)

        print(f"Image type: {type(img)}")

        result = model.generate_content([img, prompt])
        response_text = result.text
        chat_history[user_id].append({"role": "model", "parts": response_text})
        # os.remove(img_path)
    else:
        chat = model.start_chat(history=chat_history[user_id])
        response = chat.send_message(user_message)
        chat_history[user_id].append({"role": "model", "parts": response.text})
        response_text = response.text

    return response_text
