import logging
import asyncio
from docx import Document
from docx.shared import Inches
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

bot = Bot(token="6153863747:AAG8MOepJUDOs2p-lTRjhDUtv2KxYnMJzEQ")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
    name = State()
    race_type = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Здравствуй! Я бот для записи на марафон. Напиши свое ФИО.")

    await Form.name.set()


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Полумарафон'))
    keyboard.add(types.KeyboardButton('Марафон'))
    await message.reply("Выбери тип забега:", reply_markup=keyboard)

    await Form.next()


@dp.message_handler(Text(equals=['Полумарафон', 'Марафон']), state=Form.race_type)
async def process_race_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['race_type'] = message.text
        document = Document('marathon_records.docx')
        document.add_paragraph(name + ' - ' + race_type)
        document.save('marathon_records.docx')
        text = f"Ты записался на {data['race_type']}! Удачи на марафоне, {data['name']}!"
        await bot.send_message(message.chat.id, text, parse_mode=ParseMode.HTML)

        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
