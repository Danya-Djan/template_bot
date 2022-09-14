from random import random
from aiogram import Dispatcher, types
from create_bot import dp, bot
from keyboards import kb_apply, kb_register, kb_number, kb_qr
from aiogram.dispatcher.filters import Text
import re
import random
import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials



class new_user(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()
    phone = State()
    email = State()


async def command_start(message : types.Message):
    await new_user.name.set()
    await bot.send_message(message.from_user.id, "Введите своё имя:", reply_markup=types.ReplyKeyboardRemove())
async def add_name(message : types.Message, state:FSMContext):
    if not message.text.isalpha():
       await message.answer("Пожалуйста, введите имя корректно")
       return
    await state.update_data(name=message.text)
    await new_user.next()
    await bot.send_message(message.from_user.id, "Введите свою фамилию:")
async def add_surname(message : types.Message, state:FSMContext):
    if not message.text.isalpha():
       await message.answer("Пожалуйста, введите фамилию корректно")
       return
    await state.update_data(surname=message.text)
    await new_user.next()
    await bot.send_message(message.from_user.id, "Введите своё отчество:")
async def add_patronymic(message : types.Message, state:FSMContext):
    if not message.text.isalpha():
       await message.answer("Пожалуйста, введите отчество корректно")
       return
    await state.update_data(patronymic=message.text)
    await new_user.next()
    await bot.send_message(message.from_user.id, "Отправьте свой номер телефона", reply_markup=kb_number)
async def add_number(message : types.Message, state:FSMContext):
    await state.update_data(phone_number=message.contact['phone_number'])
    await state.update_data(TG_id=message.contact['user_id'])
    await new_user.next()
    await bot.send_message(message.from_user.id, "Пожалуйста, введите свой e-mail адрес:", reply_markup=types.ReplyKeyboardRemove())
async def add_email(message : types.Message, state:FSMContext):
    if not re.match('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', message.text):
        await message.answer("Пожалуйста, введите почту корректно")
        return
    await state.update_data(email=message.text)
    user_data = await state.get_data()
    print(user_data)
    await bot.send_message(message.from_user.id, f"Поздравляю, вы зарегистрированы! \n\nВаши данные: \n ФИО: {user_data['surname']} {user_data['name']} {user_data['patronymic']} \n Номер телефона:  {user_data['phone_number']} \n e-mail адрес: {user_data['email']}") #, reply_markup=kb_qr)
    await state.finish()








def register_handlers(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(add_name, state=new_user.name)
    dp.register_message_handler(add_surname, state=new_user.surname)
    dp.register_message_handler(add_patronymic, state=new_user.patronymic)
    dp.register_message_handler(add_number, content_types=types.ContentType.CONTACT, state=new_user.phone)
    dp.register_message_handler(add_email, state=new_user.email)
