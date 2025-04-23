import os
import threading
from telethon import TelegramClient, events
from http.server import BaseHTTPRequestHandler, HTTPServer

# === Настройки Telegram бота ===
api_id = 26861283
api_hash = '25b1a58fc5efb377b2dfb02672fdd9c5'
bot_token = '7472984810:AAHOROGgrsl1-bNRrni3Vt9ya5oY2onEEqM'

# === Создаём клиента
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# === Обработчик сообщений
@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    message = event.raw_text
    print(f"\n--- Новое сообщение ---")
    print(f"От: {sender.username} (ID: {sender.id})")
    print(f"Текст: {message}")
    await event.reply("✅ Привет! Бот на Render работает.")

# === Простой HTTP-сервер, чтобы Render не останавливал процесс
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running!')

def run_web_server():
    port = int(os.environ.get("PORT", 10000))  # Render передаёт PORT через переменные окружения
    server = HTTPServer(('', port), SimpleHandler)
    print(f"[🌐] Веб-сервер запущен на порту {port}")
    server.serve_forever()

# === Запуск
if __name__ == '__main__':
    threading.Thread(target=run_web_server).start()
    print("[🤖] Запускаем Telegram-бота...")
    print("[👂] Ожидаем входящие сообщения...")
    client.run_until_disconnected()
