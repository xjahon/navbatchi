import pytz
import logging
import json
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types, executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.contrib.fsm_storage.memory import MemoryStorage


BOT_TOKEN = "6331917784:AAGPPNOr1GgCRYD7tWoEVGQk79Gcd1vbRPU" # Bot toekn
ADMINS = ["473305817"]  # adminlar ro'yxati
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()
scheduler.start()
IST = pytz.timezone('Asia/Tashkent')
date = datetime.now(IST)
kun = date.strftime('%a')

week = {
    'Mon': "Dushanba",
    'Tue': "Seshanba ",
    'Wed': "Chorshanba",
    'Thu': "Payshanba",
    'Fri': "Juma",
    'Sat': "Shanba",
    'Sun': "Yakshanba"
}

f = open('kv.json')
data = json.load(f)

def func(kun):
    txt = f"<b>{week[kun]}</b>\n{data[kun][0]['user']} siz bugun navbatchisiz! \nMenyuda: {data[kun][0]['food']}"
    return txt
f.close()

def cleaner(kun):
    txt = f"Bugun <b>{week[kun]}</b> tozalik kuni!\n"
    for u in data:
        # print(u)
        txt += f"{data[u][0]['user']} "
        txt += f"siz <b>{data[u][0]['work']}</b>\n"
    # txt = f"<b>{week[kun]}</b>\n{data[kun][0]['user']} siz bugun navbatchisiz! \nMenyuda: {data[kun][0]['food']}"
    return txt
f.close()

async def send_message():
        text1 = func(datetime.today().strftime('%a'))
        text2 = cleaner(datetime.today().strftime('%a'))
        # await bot.send_message(chat_id=-1001976583662, text=text)
        await bot.send_message(chat_id=473305817, text=text1)
        if datetime.today().strftime('%a') == "Sat":
            await bot.send_message(chat_id=473305817, text=text2)
        await asyncio.sleep(0.05)

# scheduler.add_job(send_message, "interval", seconds=2)
scheduler.add_job(send_message, "interval", seconds=20)


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Bot ishga tushdi")
        except Exception as err:
            logging.exception(err)

async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
    scheduler.start()
