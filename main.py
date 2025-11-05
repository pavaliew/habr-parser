import asyncio
import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile, Message
from aiogram.utils.markdown import hbold

from parser import parse_habr_comments
from wordcloud_gen import generate_wordcloud_image
from utils import async_check_link



load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    raise ValueError("Не найден токен бота. Убедитесь, что он задан в .env файле как BOT_TOKEN")

# Инициализация бота и диспетчера
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode="HTML")



@dp.message(CommandStart())
async def command_start_handler(message: Message):
    """
    Хендлер для обработки команды /habr-user

    """
    await message.answer(f"Привет, {hbold(message.from_user.full_name)}! Отправь мне команду /habr и ссылку на профиль пользователя Habr.")



@dp.message(Command("habr-user"))
async def habr_command_handler(message: Message):
    """
    Хендлер для обработки команды /habr-user
    """
    # Разбиваем сообщение на команду и аргументы
    try:
        url = message.text.split(maxsplit=1)[1]
    except IndexError:
        await message.answer("Пожалуйста, укажите ссылку на профиль Habr после команды /habr.")
        return

    # Простая проверка на то, что это ссылка на Habr
    if not url.startswith(("http://habr.com/", "https://habr.com/")):
        await message.answer("Пожалуйста, укажите корректную ссылку на профиль пользователя Habr.")
        return

    await message.answer("Начинаю обработку... Это может занять некоторое время.")

    try:
        # 1. Запуск парсера
        comments_words = parse_habr_comments(url)
        if not comments_words:
            await message.answer("Не удалось найти комментарии на странице пользователя")
            return

        # 2. Генерация облака слов
        image_path = generate_wordcloud_image(comments_words)

        # 3. Отправка изображения пользователю
        photo = FSInputFile(image_path)
        await message.answer_photo(photo, caption="Ваше облако слов по комментариям на Habr готово!")
        
        # 4. Удаление временного файла изображения
        os.remove(image_path)

    except Exception as e:
        logging.error(f"Ошибка при обработке запроса: {e}")
        await message.answer("Произошла ошибка во время обработки вашего запроса. Попробуйте позже.")


async def main():
    """
    Основная функция для запуска бота.
    """
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
