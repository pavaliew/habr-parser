from transformers import pipeline
from collections import Counter



sentiment_analyzer = pipeline("sentiment-analysis", model="cointegrated/rubert-tiny-sentiment-balanced")



def analyze_sentiments_in_bulk(comments: list[str]) -> dict:
    """
    Анализирует тональность списка комментариев и возвращает статистику.

    :param list[str] comments: Список строк с комментариями.
    :return: Словарь со статистикой, включая количество и процентное соотношение.
    :rtype: dict
    """

    if not comments:
        return {
            "total": 0,
            "counts": {"positive": 0, "negative": 0, "neutral": 0},
            "percentages": {"positive": 0.0, "negative": 0.0, "neutral": 0.0}
        }

    results = sentiment_analyzer(comments)
    
    labels = [result['label'] for result in results]
    sentiment_counts = Counter(labels)
    
    total_comments = len(comments)
    
    positive_percentage = (sentiment_counts.get('positive', 0) / total_comments) * 100
    negative_percentage = (sentiment_counts.get('negative', 0) / total_comments) * 100
    neutral_percentage = (sentiment_counts.get('neutral', 0) / total_comments) * 100
    
    analysis_result = {
        "total": total_comments,
        "counts": {
            "positive": sentiment_counts.get('positive', 0),
            "negative": sentiment_counts.get('negative', 0),
            "neutral": sentiment_counts.get('neutral', 0)
        },
        "percentages": {
            "positive": round(positive_percentage, 2),
            "negative": round(negative_percentage, 2),
            "neutral": round(neutral_percentage, 2)
        }
    }
    
    return analysis_result



def get_analytics(comments: list[str]) -> str:
    analytics = analyze_sentiments_in_bulk(comments)

    answer = \
    f"""
Всего проанализировано комментариев: {analytics['total']}
\n--- Статистика по количеству ---
Позитивных: {analytics['counts']['positive']}
Негативных: {analytics['counts']['negative']}
Нейтральных: {analytics['counts']['neutral']}
\n--- Процентное соотношение ---
Позитивные: {analytics['percentages']['positive']}%
Негативные: {analytics['percentages']['negative']}%
Нейтральные: {analytics['percentages']['neutral']}%
    """

    return answer