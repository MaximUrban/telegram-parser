import os
from telethon import TelegramClient, events

# Получаем данные из переменных окружения
api_id = int(os.environ['26861283'])
api_hash = os.environ['25b1a58fc5efb377b2dfb02672fdd9c5']
bot_token = os.environ['7472984810:AAHOROGgrsl1-bNRrni3Vt9ya5oY2onEEqM']

# Создаем клиент
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Пример обработчика входящих сообщений
@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    message = event.raw_text
    print(f"Сообщение от {sender.id}: {message}")
    await event.reply("Привет! Бот работает на Render 🎉")

# Запускаем клиента
with client:
    print("Бот запущен.")
    client.run_until_disconnected()
