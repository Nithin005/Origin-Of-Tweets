import re
from rake_nltk import Rake

def match_keywords(keywords, text):
    """
    Searches the text for keywords, returning the no of matches found
    
    Parameters:
    keywords (list(str)): list of keywords
    text (str): text to be searched in

    Returns:
    int: no_of_keywords_matched / len(keywords)
    """
    if(len(keywords) == 0):
        return 0
    matches = 0
    for key in keywords:
        res = re.search(key, text)
        if(res):
            matches += 1
    return matches/len(keywords)


def calc_metric(keywords, text, timestamp):
    """
    calculates the metric based on both time and keywords matched

    Parameters:
    keywords (list(str)): list of keywords
    text (str): text to be searched in

    Returns:
    int: keywords_metric / timestamp
    """
    _a = match_keywords(keywords, text)
    _b = timestamp / 10**15
    return _a / _b

def extract_keywords(text):
    r = Rake()
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases_with_scores()
    results = []
    for key in keywords:
        if(key[0] > 1):
            text = key[1]
            if(len(text.split())<=2):
                results.append(text)

    return results

