import json
import os
from pathlib import Path
from .objects import *

TECHNIQUE_DIRECTORY = Path(__file__).parent.parent / 'techniques'

def fetch_all_ids() -> list[str]:
    files = os.listdir(TECHNIQUE_DIRECTORY)
    return [f.replace('.json', '') for f in files]

def fetch(id: str) -> Technique | None:
    path = TECHNIQUE_DIRECTORY / (id + '.json')
    if not os.path.exists(path): return None
    with open(path, mode='r', encoding='utf-8') as f:
        return Technique.deserialize(f.read())

def find(id: str):
    technique = fetch(id)
    assert technique
    return technique

def create(technique: Technique):
    assert fetch(technique.id) == None
    save(technique)

def update(technique: Technique):
    assert find(technique.id)
    save(technique)

def save(technique: Technique):
    path = TECHNIQUE_DIRECTORY / (technique.id + '.json')
    with open(path, mode='w', encoding='utf-8') as f:
        contents = technique.serialize()
        json.dump(contents, f, indent=4)
        print(f'Saved {technique.id}')

def delete(technique: Technique):
    assert find(technique.id)
    path = TECHNIQUE_DIRECTORY / (technique.id + '.json')
    os.remove(path)
    print(f'Deleted {technique.id}')

def clean():
    ids = fetch_all_ids()
    for id in ids:
        technique = find(id)
        
        # Clean parent
        if technique.parent:
            other_technique = fetch(technique.parent)
            # Parent doesn't exist, remove it exists, make sure the inversion is mutual
            if not other_technique:
                technique.parent = None

        # Clean inverse
        if technique.inverse:
            other_technique = fetch(technique.inverse)
            # Inverse exists, make sure the inversion is mutual
            if other_technique:
                assert not other_technique or other_technique.inverse == technique.id
                other_technique.inverse = technique.id
                save(other_technique)
            # Inverse doesn't exist, remove it
            else:
                technique.inverse = None

        # Clean follow ups
        technique.followups = [x for x in technique.followups if fetch(x)]
        for x in technique.followups:
            other_technique = find(x)
            if technique.id in other_technique.preceding: continue
            other_technique.precending.append(technique.id)
            save(other_technique)

        # Clean preceding
        technique.precending = [x for x in technique.preceding if fetch(x)]
        for x in technique.preceding:
            other_technique = find(x)
            if technique.id in other_technique.followups: continue
            other_technique.followups.append(technique.id)
            save(other_technique)

__all__ = ['fetch_all_ids', 'fetch', 'find', 'create', 'update', 'save', 'delete', 'clean']