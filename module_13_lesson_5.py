# Импорты
# --------------------------------------------------------------------------------------------------

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

import asyncio
# --------------------------------------------------------------------------------------------------

# Классы
# --------------------------------------------------------------------------------------------------
class UserState(StatesGroup):
    age = State()
    growth  = State()
    weight = State()
    # sex = State()
# --------------------------------------------------------------------------------------------------

# Настройки бота
# --------------------------------------------------------------------------------------------------
api = "???"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# Клавиатура
kb = ReplyKeyboardMarkup()
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
kb.add(button_1)
kb.add(button_2)
kb.resize_keyboard = True
# --------------------------------------------------------------------------------------------------

# Работа бота
# --------------------------------------------------------------------------------------------------
@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий вашему здоровью.'
        ' Нажмите "Рассчитать", чтобы узнать вашу суточную норму'
        ' потребления килокалорий.'
        ' Нажмите "Информация", чтобы узнать подробнее.', reply_markup = kb)

# Обработка кнопки Информация
# --------------------------------------------------------------------------------------------------
@dp.message_handler(text = ['Информация'])
async  def info_messages(message):
    await message.answer(
        'Данный бот подсчитывает норму потребления калорий для мужчин и женщин по'
        ' упрощённой формуле Миффлина - Сан Жеора'
        ' (https://www.calc.ru/Formula-Mifflinasan-Zheora.html).')

# Обработка кнопки Рассчитать. Запуск расчёта калорий
# --------------------------------------------------------------------------------------------------
@dp.message_handler(text=['Рассчитать'])
async def set_age(message):

    await message.answer('Введите свой возраст (целое число):')
    await UserState.age.set()

# Запрашиваем возраст
# --------------------------------------------------------------------------------------------------
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):

    # Можно сделать через try except
    if not any(map(str.isdigit, message.text)):
        await message.answer('Вы ввели не число. Пожалуйста, повторите ввод. Укажите возраст:')
        return
    else:
        age = int(abs(float(message.text)))

    await state.update_data(age = age)

    # Для пробы воспользовался reply
    await message.reply(f'Вы указали свой возраст: {age}')
    await message.answer('Введите свой рост в сантиметрах (целое число):')
    await UserState.growth.set()


# Запрашиваем рост
# --------------------------------------------------------------------------------------------------
@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):

    if not any(map(str.isdigit, message.text)):
        await message.answer('Вы ввели не число. Пожалуйста, повторите ввод. Укажите рост:')
        return
    else:
        growth = int(abs(float(message.text)))

    await state.update_data(growht = growth)
    await message.answer(f'Вы указали свой рост: {growth}')
    await message.answer('Введите свой вес в килограммах (целое число):')
    await UserState.weight.set()

# Запрашиваем вес и производим рассчёт
# --------------------------------------------------------------------------------------------------
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

# Обработка всех прочих сообщений
# --------------------------------------------------------------------------------------------------
@dp.message_handler()
async  def all_messages(message):

    await message.answer('Введите /start, чтобы запустить калькулятор.')
# --------------------------------------------------------------------------------------------------

# Запуск бота
# --------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

# Постарался предупредить ошибки. Для ввода доступны только числа.
# При неверном вводе запрашивает значение повторно.
# Далее переводится в число с плавающей точкой. Берётся абсолютное значение числа.
# Потом переводится в целое число (хотя можно и без этого).
# Есть недочеты. Например: введёное значение 85_5 преобразуется в 855.
# Просто дальше стало лень, так как не требуется заданием.