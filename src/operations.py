import json
import os
from pathlib import Path
from .objects import *

ARTICLE_DIRECTORY = Path(__file__).parent.parent / 'articles'
ID_REGISTRY_FILE = '_ids.json'

def fetch_all_ids() -> list[str]:
    files = os.listdir(ARTICLE_DIRECTORY)
    return [f.replace('.json', '') for f in files if f != ID_REGISTRY_FILE]

def fetch(id: str) -> Article | None:
    path = ARTICLE_DIRECTORY / (id + '.json')
    if not os.path.exists(path): return None
    with open(path, mode='r', encoding='utf-8') as f:
        return Article.deserialize(f.read())

def find(id: str):
    article = fetch(id)
    assert article
    return article

def create(article: Article):
    assert fetch(article.id) == None
    save(article)

def update(article: Article):
    assert find(article.id)
    save(article)

def save(article: Article):
    path = ARTICLE_DIRECTORY / (article.id + '.json')
    with open(path, mode='w', encoding='utf-8') as f:
        contents = article.serialize()
        json.dump(contents, f, indent=4)
        print(f'Saved {article.id}')

def delete(article: Article):
    assert find(article.id)
    path = ARTICLE_DIRECTORY / (article.id + '.json')
    os.remove(path)
    print(f'Deleted {article.id}')

def clean():
    ids = fetch_all_ids()

    # Save id registry file
    with open(ARTICLE_DIRECTORY / ID_REGISTRY_FILE, mode='w', encoding='utf-8') as f:
        json.dump(ids, f)

    for id in ids:
        article = find(id)
        article.id = id
        
        # Clean parent
        if article.parent:
            other_article = fetch(article.parent)
            # Parent doesn't exist, remove it exists, make sure the inversion is mutual
            if not other_article:
                print(id, 'Parent does not exist, removing parent', article.parent)
                article.parent = None

        # Clean inverse
        if article.inverse:
            other_article = fetch(article.inverse)
            # Inverse exists, make sure the inversion is mutual
            if other_article:
                if not other_article.inverse:
                    print(id, 'Inverse is not mutual, adding inverse on mirror', other_article.inverse)
                    other_article.inverse = article.id
                elif other_article.inverse != article.id:
                    print(id, 'Inverse points to another article, error', other_article.id, other_article.inverse)
                    assert False
            # Inverse doesn't exist, remove it
            else:
                print(id, 'Inverse does not exist, removing inverse', article.inverse)
                article.inverse = None

        # Clean follow ups
        article.followups = [x for x in article.followups if fetch(x)]

        # Clean counters
        article.counters = [x for x in article.counters if fetch(x)]

        # Clean concepts
        article.concepts = [x for x in article.concepts if fetch(x)]

        update(article)

__all__ = ['fetch_all_ids', 'fetch', 'find', 'create', 'update', 'save', 'delete', 'clean']