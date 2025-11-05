def generate_wordcloud_image(words: list) -> str:
    """Функция-заглушка для генерации облака слов. Возвращает путь к файлу."""
    print("Генерация облака слов...")
    # Здесь ваш код генерации изображения
    # Он должен сохранить файл и вернуть путь к нему
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    text = " ".join(words)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    
    image_path = "habr_wordcloud.png"
    wordcloud.to_file(image_path)
    return image_path
