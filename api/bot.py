import asyncio
import requests
from const import BOT_TOKEN as TOKEN
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

API_TOKEN = TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
SSH_IP = '89.223.126.79:8000'

class UserStates(StatesGroup):
    register = State()
    subscribe = State()
    message = State()


async def get_token(id):
    token_api_url = f'http://{SSH_IP}/api/get_token/'
    data = {'user_id': id}
    response = requests.post(url=token_api_url, json=data)
    if response.status_code == 200:
        token = response.json().get('message')
        return token


@dp.message(Command('register'))
async def register_command(message: Message):
    args = message.text.split()
    if len(args) != 4:
        await message.reply("Неправильный формат команды. Используйте: /register username password first_name")
        return
    username, password, first_name = args[1], args[2], args[3]
    api_url = f'http://{SSH_IP}/api/register/'
    user_data = {
        'username': username,
        'password': password,
        'first_name': first_name,
        'user_id_from_telegram': message.from_user.id
    }
    response = requests.post(api_url, json=user_data)
    print(response.content)
    response_data = response.json()
    message_content = response_data.get('message', 'Сообщение не найдено')
    if response.status_code == 201:
        await message.reply(message_content)
    else:
        await message.reply(message_content)


@dp.message(Command('start'))
async def start_command(message: Message):
    await message.reply("Привет! Я ваш Telegram бот. Меня зовут wishper. Для регестраци, используйте /register")


@dp.message(Command('subscribe'))
async def subscribe_command(message: Message):
    user_id = message.from_user.id
    api_url = f'http://{SSH_IP}/api/subscribe/'
    auth_token = await get_token(id=user_id)
    headers = {
        'Authorization': f'Token {auth_token}',
        'Content-Type': 'application/json',
    }
    response = requests.post(api_url, headers=headers)
    if response.status_code == 201:
        await message.reply("Спасибо за подписку! Теперь вы подписаны на нашего бота.")
    elif response.status_code == 400:
        await message.reply("Вы уже подписаны.")
    else:
        await message.reply("Произошла ошибка при подписке.")


@dp.message(Command('my_messages'))
async def messages_list(message: Message):
    auth_token = await get_token(id=message.from_user.id)
    headers = {
        'Authorization': f'Token {auth_token}',
        'Content-Type': 'application/json',
    }
    api_url = f'http://{SSH_IP}/api/messages_list/'
    response = requests.post(url=api_url, headers=headers)
    messages = response.json()
    for message_data in messages:
        await message.reply(f"{message_data['timestamp']}\n{message_data['content']}")


@dp.message()
async def message(message: Message):
    message_content = message.text
    api_url = f'http://{SSH_IP}/api/send_message/'
    data = {"message": message_content}
    auth_token = await get_token(id=message.from_user.id)
    headers = {
        'Authorization': f'Token {auth_token}',
        'Content-Type': 'application/json',
    }
    response = requests.post(url=api_url, json=data, headers=headers)
    if response.status_code == 200:
        await message.reply(message_content)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
