import string
from pymorphy3 import MorphAnalyzer
import algorithm.stopwords


class Lemmatizer:
    def __init__(self):
        self.morph = MorphAnalyzer()
        self.stopwords_ru = algorithm.stopwords.get_stopwords()


    def lemmatize(self, input: str) -> list:
        if input!='':
            tokens = []
            input = input.translate(str.maketrans({key: ' ' for key in string.punctuation}))
            for token in input.split():
                if token:
                    token = token.strip()
                    token = self.morph.normal_forms(token)[0]
                    pos = self.morph.parse(token)[0].tag.POS
                    if pos == 'NOUN' and token not in self.stopwords_ru:
                        tokens.append(token)
            if len(tokens) > 2:
                return tokens

        return None

