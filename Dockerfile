
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
ENV GEMINI_API_KEY=${GEMINI_API_KEY}


EXPOSE 8080


CMD ["python", "main.py"]
