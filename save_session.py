from telethon.sync import TelegramClient

api_id = 29840156
api_hash = '3473b0f92b274f13f1b351b8f5b67b46'
bot_token = '6933794436:AAE7lvbViCeE9LgSmHgk8AfTflwQGLD2-JY'

with TelegramClient('bot', api_id, api_hash) as client:
    client.start(bot_token=bot_token)
    print("Сессия сохранена в файл bot.session")
