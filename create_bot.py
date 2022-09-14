from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()


bot = Bot(token="5441021839:AAHNcSgSzRpl6uhZsIIANsUdKYUGpV0EGyY")
dp = Dispatcher(bot, storage=storage)