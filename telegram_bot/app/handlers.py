from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.middlewares import TestMiddleware

router = Router()

router.message.outer_middleware(TestMiddleware())


class Reg(StatesGroup):
    name = State()
    number = State()



@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f'Привет. \nТвой ID: {message.from_user.id}\nИмя: {message.from_user.first_name}',
                        reply_markup=kb.main)


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Это команда /help')


@router.message(F.text == 'Как дела?')
async def how_are_you(message: Message):
    await message.answer('OK!')


@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(F'ID фото: {message.photo[-1].file_id}')


@router.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAMcZg_WO3DaWFU6HSJvkGW7KZhb1MwAAoXYMRvsR4BIDLrPsuqWPgIBAAMCAAN4AAM0BA',
                               caption='Это СерГЕЙ')


@router.callback_query(F.data == 'catalog')
async def catalog(callback: CallbackQuery):
    await callback.answer('Вы выбрали каталог' , show_alert=True)
    await callback.message.edit_text('Привет', reply_markup=await kb.inline_cars())


@router.message(Command('reg'))
async def reg_one(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите Ваше имя')


@router.message(Reg.name)
async def reg_two(message:Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer('Введите номер телефона')


@router.message(Reg.number)
async def two_three(message: Message, state:FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f'Спасибо.Регистрация завершена.\nИмя:{data["name"]}\nНомер: {data["number"]}')
    await state.clear()
