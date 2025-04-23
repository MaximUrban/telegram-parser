import os
import threading
from telethon import TelegramClient, events
from http.server import BaseHTTPRequestHandler, HTTPServer

# === Настройки Telegram бота ===
api_id = 26861283
api_hash = '25b1a58fc5efb377b2dfb02672fdd9c5'
bot_token = '7472984810:AAHOROGgrsl1-bNRrni3Vt9ya5oY2onEEqM'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    message = event.raw_text
    print(f"Сообщение от {sender.id}: {message}")
    await event.reply("Привет! Бот работает на Render 🎉")

# === Фейковый веб-сервер ===
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running!')

def run_web_server():
    port = int(os.environ.get("PORT", 10000))  # Render автоматически передает PORT
    server = HTTPServer(('', port), SimpleHandler)
    print(f"Фейковый веб-сервер запущен на порту {port}")
    server.serve_forever()

# === Запускаем всё ===
if __name__ == '__main__':
    threading.Thread(target=run_web_server).start()
    print("Запускаем Telegram-бота...")
    client.run_until_disconnected()
