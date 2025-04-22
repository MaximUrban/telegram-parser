from telethon.sync import TelegramClient
from telethon.tl.functions.contacts import SearchRequest

api_id = 123456  # замени на своё
api_hash = 'your_api_hash'  # замени на своё
client = TelegramClient('session', api_id, api_hash)

async def search():
    await client.start()
    result = await client(SearchRequest(q='подарки', limit=10))
    for chat in result.chats:
        print(chat.title, chat.username)

with client:
    client.loop.run_until_complete(search())
