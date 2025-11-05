import requests
from bs4 import BeautifulSoup as bs



def parse_habr_comments(url: str) -> list[str]:
    """
    Функция для парсинга страницы с комментариями пользователя Habr

    :param str url: Ссылка на страницу пользователя
    :return: Список комментариев
    :rtype: list[str]
    """

    print(f"Парсинг начался: {url}")
    
    response = requests.get(f"{(url[:-1] if url.endswith("/") else url)}/comments/")
    soup = bs(response.content, "lxml")

    comments = []
    try:
        comments = [
            comment.find(class_="tm-comment__body-content").text.strip() 
            for comment in soup.find(class_="tm-user-comments").find_all(class_="tm-user-comment-card")
        ]
        # print(comments)
        pagination = soup.find(class_="tm-pagination")
        if pagination is not None:
            pagination = int(pagination.find_all(class_="tm-pagination__page")[-1].text)
            # print(pagination)
            for i in range(2, pagination + 1):
                response = requests.get(f"{(url[:-1] if url.endswith("/") else url)}/comments/page{i}/")
                soup_inner = bs(response.content, "lxml")
                
                comments.extend([
                    comment.find(class_="tm-comment__body-content").text.strip() 
                    for comment in soup_inner.find(class_="tm-user-comments").find_all(class_="tm-user-comment-card")
                ])
        
        
    except Exception as e:
        # print(e.with_traceback())
        comments = []
    finally:
        print(f"Парсинг завершен: {url}")
        return comments

