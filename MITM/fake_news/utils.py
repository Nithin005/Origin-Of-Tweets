import string

from joblib import dump, load

from origin_finder.logger import logger

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop = stopwords.words('english')

import os.path
path = os.path.dirname(__file__)

model = load(os.path.join(path, 'decision_tree_classifier.joblib'))

def punctuation_removal(text):
    all_list = [char for char in text if char not in string.punctuation]
    clean_str = ''.join(all_list)
    return clean_str

def stopword_removal(text):
    return ' '.join([word for word in text.split() if word not in (stop)])

def preprocess_one(text):
    logger.debug(f'preprocess_one() before: {text}')
    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = punctuation_removal(text)

    #Remove stopwords
    text = stopword_removal(text)
    logger.debug(f'preprocess_one() after: {text}')
    return text

def predict_one(text):
    text = preprocess_one(text)
    res = model.predict([text])
    return res[0]
