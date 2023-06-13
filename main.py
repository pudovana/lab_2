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
