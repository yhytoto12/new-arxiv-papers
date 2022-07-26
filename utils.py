import json
import requests

def check_keyword(keyword, paper):
    # check if a keyword is in paper's title or abstract
    if isinstance(keyword, str):
        return keyword.lower() in paper['title'].lower() or keyword.lower() in paper['abstract']

    # check if ALL keywords are in title or abstract
    elif isinstance(keyword, tuple):
        isIn = True
        for k in keyword:
            if k.lower() not in paper['title'].lower() and k.lower() not in paper['abstract'].lower():
                isIn = False
        return isIn

    # check if ANY keyword is in title or abstract
    elif isinstance(keyword, list):
        for k in keyword:
            if k.lower() in paper['title'].lower() or k.lower() in paper['abstract'].lower():
                return True
        return False


def to_label(keyword):
    if isinstance(keyword, str):
        k = keyword

    elif isinstance(keyword, tuple):
        k = ' & '.join(keyword)

    elif isinstance(keyword, list):
        k = keyword[0]

    return k
