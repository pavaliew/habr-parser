import asyncio
import logging
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile, Message
from aiogram.utils.markdown import hbold

from parser import parse_habr_comments
from wordcloud_gen import generate_wordcloud_image
from utils import filter_comments
from analyzer import get_analytics



load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    raise ValueError("Не найден токен бота. Убедитесь, что он задан в .env файле как BOT_TOKEN")

dp = Dispatcher()
bot = Bot(
    TOKEN, 
    default=DefaultBotProperties(parse_mode='HTML')
)



@dp.message(CommandStart())
async def command_start_handler(message: Message):
    """
    Хендлер для обработки команды /start

    :param Message message: сообщение, полученное от пользователя
    :rtype: None
    """

    await message.answer(
        f"Привет, {hbold(message.from_user.full_name)}! Отправь мне команду /habr_user и ссылку на профиль пользователя Habr, чтобы получить анализ комментариев."
    )



@dp.message(Command("habr_user"))
async def habr_command_handler(message: Message):
    """
    Хендлер для обработки команды /habr_user

    :param Message message: сообщение, полученное от пользователя
    :rtype: None
    """

    try:
        url = message.text.split(maxsplit=1)[1]
    except IndexError:
        await message.answer("Пожалуйста, укажите ссылку на профиль Habr через пробел после команды /habr_user в формате http://habr.com/ru/users/username.")
        return

    if not url.startswith(("http://habr.com/ru/users", "https://habr.com/ru/users")):
        await message.answer("Пожалуйста, укажите корректную ссылку на профиль пользователя Habr.")
        return

    await message.answer("Начинаю обработку... Это может занять некоторое время.")

    try:
        comments = parse_habr_comments(url)
        if not comments:
            await message.answer("Не удалось найти комментарии на странице или страница недоступна.")
            return
        
        filtered_words = filter_comments(comments)

        image_path = generate_wordcloud_image(filtered_words)

        photo = FSInputFile(image_path)
        await message.answer_photo(photo, caption="Облако слов по комментариям пользователя на Habr готово!")

        os.remove(image_path)

        analytics_result = get_analytics(comments)
        await message.answer("Анализ комментариев пользователя готов!")
        await message.answer(analytics_result)



    except Exception as e:
        logging.error(f"Ошибка при обработке запроса: {e}")
        await message.answer("Произошла ошибка во время обработки вашего запроса. Попробуйте позже.")



async def main():
    """
    Основная функция для запуска бота.

    :rtype: None
    """
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
