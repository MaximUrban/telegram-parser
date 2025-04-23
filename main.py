from telethon import TelegramClient, events
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors import FloodWaitError
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import threading
import time
import pymorphy2
from rapidfuzz import process

api_id = 26861283
api_hash = '25b1a58fc5efb377b2dfb02672fdd9c5'
bot_token = '7472984810:AAHOROGgrsl1-bNRrni3Vt9ya5oY2onEEqM'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
morph = pymorphy2.MorphAnalyzer()
user_states = {}

@client.on(events.NewMessage(pattern='/parser'))
async def start_parser(event):
    user_id = event.sender_id
    user_states[user_id] = 'awaiting_query'
    await event.respond("Напиши тематику или запрос для парсинга")

@client.on(events.NewMessage)
async def message_handler(event):
    user_id = event.sender_id
    message = event.raw_text.strip()

    if user_states.get(user_id) == 'awaiting_query':
        query = normalize_text(message)
        user_states.pop(user_id)

        await event.respond(f"Ищу каналы по запросу: {query}...")
        channels = await search_channels(query)
        if channels:
            response = '\n\n'.join(channels)
        else:
            response = "Не удалось найти подходящие каналы 😕"
        await event.respond(response)

def normalize_text(text):
    words = text.lower().split()
    normalized = [morph.parse(w)[0].normal_form for w in words]
    return ' '.join(normalized)

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
        for user in result.chats:
            if getattr(user, 'megagroup', False):  # это супергруппа, не канал
                continue
            if getattr(user, 'broadcast', False) and user.participants_count >= 1000:
                link = f"https://t.me/{user.username}" if user.username else user.title
                channels.append(f"{user.title} — {link} ({user.participants_count} подписчиков)")

        return channels
    except FloodWaitError as e:
        await asyncio.sleep(e.seconds)
        return []
    except Exception as e:
        print(f"Ошибка при поиске каналов: {e}")
        return []

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running!')

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('', port), SimpleHandler)
    print(f"Фейковый веб-сервер запущен на порту {port}")
    server.serve_forever()

if __name__ == '__main__':
    threading.Thread(target=run_web_server).start()
    print("Запускаем Telegram-бота...")
    client.run_until_disconnected()
