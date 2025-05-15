import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.utils.chat_action import ChatActionSender
from aiogram.utils.media_group import MediaGroupBuilder
import sys


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
dp = Dispatcher()


async def cats():
    bot = Bot(token='8024246712:AAHtWKMJ76FA0SCK5oDRYPiAjKucF0sObvY')
    await dp.start_polling(bot)


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    global rent
    await message.reply("Вы хотите увидеть фото котят? Вы готовы?")

    # небольшая пауза
    await asyncio.sleep(1)

    # Хорошая практика отправлять в chat actions... (действия бота)
    async with ChatActionSender.upload_photo(bot=message.bot, chat_id=message.chat.id):
        # Создаем медиа группу для картинок
        media = MediaGroupBuilder(caption="CATS")

        # Добавляем локальный файл
        media.add_photo('https://cataas.com/cat/says/hello', 'Случайный кот.')
        await asyncio.sleep(1)
        # Еще локальный файл
        media.add_photo('https://cataas.com/cat', 'Случайный кот.')
        await asyncio.sleep(1)
        # Можно также использовать URL'ы
        media.add_photo('https://cataas.com/cat', 'Случайный кот.')
        # Готово! Отправляем группу картинок
        await asyncio.sleep(1)
        await message.reply_media_group(media=media.build())


if __name__ == '__main__':
    asyncio.run(cats())