from src import *

t = Technique(
    id='triangle',
    name='Triangle',
    name_suffix_1=None,
    name_suffix_2=None,
    other_names=None,
    summary='TODO',
    types=[TechniqueType.SUBMISSION_CHOKEHOLD],
    difficulty=TechniqueDifficulty.UNIVERSAL,
    is_counter=False,
    requires_gi=False,
    ranking=0,
    is_searchable=True,
    parent=None,
    inverse=None,
    followups=[],
    preceding=[],
    concepts=[],
    content=[]
)

create(t)
# update(t)
clean()