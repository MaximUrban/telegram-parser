import os
import threading
from telethon import TelegramClient, events
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.types import InputPeerEmpty, Channel
from http.server import BaseHTTPRequestHandler, HTTPServer

# === Настройки бота ===
api_id = 29840156
api_hash = '3473b0f92b274f13f1b351b8f5b67b46'

client = TelegramClient('bot', api_id, api_hash)
client.start()

# Состояние пользователей
user_states = {}

# === Обработчик команды /parser ===
@client.on(events.NewMessage(pattern='/parser'))
async def parser_command(event):
    user_id = event.sender_id
    user_states[user_id] = 'awaiting_query'
    await event.reply("✏️ Напиши тематику или запрос для парсинга.")

# === Обработчик всех остальных сообщений ===
@client.on(events.NewMessage)
async def handle_message(event):
    user_id = event.sender_id
    text = event.raw_text.strip()

    # Игнорируем собственные ответы
    if event.out:
        return

    # Если ждём тему от пользователя
    if user_states.get(user_id) == 'awaiting_query':
        user_states.pop(user_id)
        await event.reply(f"🔍 Ищу каналы по теме: {text}")
        channels = await search_channels(text)
        if channels:
            await event.reply("\n\n".join(channels[:15]), link_preview=False)
        else:
            await event.reply("😕 Ничего не нашёл. Попробуй другую формулировку.")
    else:
        await event.reply("✅ Привет! Бот на Render работает.")

# === Функция поиска каналов ===
async def search_channels(query):
    try:
        result = await client(SearchRequest(
            q=query,
            limit=50,
            offset=0,
            offset_rate=0,
            peer=InputPeerEmpty()
        ))

        channels = []
        for chat in result.chats:
            if isinstance(chat, Channel) and chat.broadcast and not chat.megagroup and chat.username and chat.participants_count and chat.participants_count >= 1000:
                link = f"https://t.me/{chat.username}"
                channels.append(f"📣 [{chat.title}]({link}) — {chat.participants_count} подписчиков")
        return channels
    except Exception as e:
        print(f"Ошибка при поиске: {e}")
        return []

# === Простой веб-сервер для Render ===
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running!')

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('', port), SimpleHandler)
    print(f"[🌐] Web-сервер запущен на порту {port}")
    server.serve_forever()

# === Запуск ===
if __name__ == '__main__':
    threading.Thread(target=run_web_server).start()
    print("[🤖] Telegram-бот запущен.")
    client.run_until_disconnected()
