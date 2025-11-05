import json
import re



stop_words_ru = None
with open("stop_words_ru.json", encoding="utf-8") as stopwords_file:
    stop_words_ru = set(json.load(stopwords_file))

letters_pattern = re.compile(r"[^         АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя a-z A-Z]")


def get_raw_text(comments: list[str]) -> str:
    return " ".join([letters_pattern.sub(r" ", comment) for comment in comments]).lower()



def filter_comments(comments: list[str]) -> str:
    """
    Фильтрация списка комментариев с использованием списка стоп-слов
    
    :param list[str] comments: Список комментариев, полученных путем парсинга страницы пользователя
    :return: Обработанная строка
    :rtype: str
    """
    
    return " ".join(list(filter(lambda x: x not in stop_words_ru, get_raw_text(comments).split())))
