import string
from collections import Counter
from sklearn.base import BaseEstimator, TransformerMixin

class Chars_encoder(BaseEstimator, TransformerMixin):

    def fit(self, password, y=None):
        return self

    def transform(self, password, y = None):
        chars = list(string.ascii_letters + '0123456789!"#$%&()*+,-./:;<=>?@[\]^_`{|}~')
        chars_in_pass_dict = Counter(password)
        encoded_data = []
        for char in chars:
            if char in chars_in_pass_dict:
                encoded_data.append(chars_in_pass_dict.get(char))
            else:
                encoded_data.append(0)
        
        return [encoded_data]





