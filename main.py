from aiogram.utils import executor

import os

from create_bot import dp



async def on_startup(_):
    print("Старт бота")

from handlers import user, admin, other

user.register_handlers(dp)
other.register_handlers(dp)



executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
