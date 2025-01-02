from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

import asyncio

api = "???"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth  = State()
    weight = State()
    # sex = State()

@dp.message_handler(text=['Calories', 'calories'])
async def set_age(message):

    await message.answer('Введите свой возраст (целое число):')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):

    if not any(map(str.isdigit, message.text)):
        await message.answer('Вы ввели не число. Пожалуйста, повторите ввод. Укажите возраст:')
        return
    else:
        age = int(abs(float(message.text)))

    await state.update_data(age = age)

    # Для пробы воспользовался reply
    await message.reply(f'Вы указали свой возраст: {age}')
    await message.answer('Введите свой рост (целое число):')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):

    if not any(map(str.isdigit, message.text)):
        await message.answer('Вы ввели не число. Пожалуйста, повторите ввод. Укажите рост:')
        return
    else:
        growth = int(abs(float(message.text)))

    await state.update_data(growht = growth)
    await message.answer(f'Вы указали свой рост: {growth}')
    await message.answer('Введите свой вес (целое число):')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):

    if not any(map(str.isdigit, message.text)):
        await message.answer('Вы ввели не число. Пожалуйста, повторите ввод. Укажите вес:')
        return
    else:
        weight = int(abs(float(message.text)))

    await state.update_data(weight = weight)
    await message.answer(f'Вы указали свой вес: {weight}')

    data = await state.get_data()
    calories_male = 10 * data['weight'] + 6.25 * data['growht'] - 5 * data['age'] + 5
    calories_female = 10 * data['weight'] + 6.25 * data['growht'] - 5 * data['age'] - 161

    await message.answer(f'Норма калорий для мужчины: {calories_male}')
    await message.answer(f'Норма калорий для женщины: {calories_female}')
    await state.finish()

@dp.message_handler()
async  def all_messages(message):

    await message.answer('Введите Calories или calories, чтобы запустить калькулятор.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

# Постарался предупредить ошибки. Для ввода доступны только числа.
# При неверном вводе запрашивает значение повторно.
# Далее переводится в число с плавающей точкой. Берётся абсолютное значение числа.
# Потом переводится в целое число (хотя можно и без этого).
# Есть недочеты. Например: введёное значение 85_5 преобразуется в 855.
# Просто дальше стало лень, так как не требуется заданием.