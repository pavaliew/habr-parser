import os
import uuid

from wordcloud import WordCloud
import matplotlib.pyplot as plt



def generate_wordcloud_image(words: str) -> str:
    """
    Генерация облака слов. Возвращает путь к файлу.

    :param str words: Строка, состоящая из предобработанных строк
    :return: Путь к файлу с облаком слов
    :rtype: str
    """

    def save_image() -> str:
        """
        Сохраняет изображение 

        :return: Путь к результирующему файлу
        :rtype: str
        """

        if not os.path.exists("temp"):
            os.makedirs("temp")

        unique_id = str(uuid.uuid4()).split('-')[0]

        image_path = f"temp/habr_wordcloud_{unique_id}.png"
        wordcloud.to_file(image_path)

        return image_path
    
    print("Генерация облака слов...")
    wordcloud = WordCloud(width=1000, height=1000, random_state=41, collocations=False).generate(words)

    return save_image()
