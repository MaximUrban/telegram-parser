from telethon import TelegramClient, events

# Вставленные данные напрямую
api_id = 26861283
api_hash = '25b1a58fc5efb377b2dfb02672fdd9c5'
bot_token = '7472984810:AAHOROGgrsl1-bNRrni3Vt9ya5oY2onEEqM'

# Создаем клиента
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Обработчик входящих сообщений
@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    message = event.raw_text
    print(f"Сообщение от {sender.id}: {message}")
    await event.reply("Привет! Бот работает на Render 🎉")

# Запуск клиента
with client:
    print("Бот запущен.")
    client.run_until_disconnected()
