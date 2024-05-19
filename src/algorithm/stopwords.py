import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

def get_stopwords() -> set:
    stopwords_ru = set(stopwords.words('russian'))

    stopwords_ru.update([
        'сообщество',
        'группа',
        'руб',
        'день',
        'год',
        'вопрос',
        'пост',
        'цель',
        'гр',
        'ул',
        'мочь',
        'паблик',
        'сайт',
        'знак',
        'цвет',
        'предложка'
    ])

    return stopwords_ru
