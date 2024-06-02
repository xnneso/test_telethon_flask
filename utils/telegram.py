from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
import os


load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

"""device_model и system_version указываю, чтобы телеграм не выкидывал из всех сессий (с чем столкнулся)"""
client = TelegramClient(StringSession(), api_id, api_hash, device_model="MS-7C37", system_version="4.16.30-vxCUSTOM")


async def connect():
    if not client.is_connected():
        await client.connect()


async def generate_qr():
    await connect()
    qr_login = await client.qr_login()
    return qr_login


async def check_qr(qr_login):
    await connect()
    await qr_login.wait()


async def authorized():
    await connect()
    return await client.is_user_authorized()


async def get_messages(user):
    await connect()
    if await authorized():
        messages = []
        owner = await client.get_me()
        async for i in client.iter_messages(user, limit=50):
            messages.append({'username': user, 'is_self': i.sender_id == owner.id, 'message_text': i.text})
        return messages
    return {'status': 'not authorized'}


async def send_message(user, message):
    await connect()
    if await authorized():
        await client.send_message(user, message)
        return {'status': 'ok'}
    return {'status': 'not authorized'}