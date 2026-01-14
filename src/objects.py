from enum import IntEnum
from typing import Any
import json

class TechniqueDifficulty(IntEnum):
    UNIVERSAL = 0
    BEGINNER = 10
    NOVICE = 20
    INTERMEDIATE = 30
    ADVANCED = 40
    EXPERT = 50

class TechniqueType(IntEnum):
    # Positions
    POSITION = 100,
    # Submissions
    SUBMISSION = 200,
    SUBMISSION_CHOKEHOLD = 201,
    SUBMISSION_JOINT_LOCK = 202,
    SUBMISSION_COMPRESSION_LOCK = 203,
    # Sweeps
    SWEEP = 300,
    # Takedowns
    TAKEDOWN = 400,
    TAKEDOWN_THROW = 401,
    # Passes
    PASS = 500,
    # Defenses
    DEFENSE = 700,
    DEFENSE_ESCAPE = 701,
    # Concepts
    CONCEPT = 900

class TechniqueContentType(IntEnum):
    TEXT = 10
    YOUTUBE_VIDEO = 30
    AD = 90

class TechniqueContent:
    def __init__(self,
        content_type: TechniqueContentType,
        contents: str,
        title: str | None,
        video_start: int | None
    ):
        self.content_Type = content_type
        self.contents = contents
        self.title = title
        self.video_start = video_start

    @staticmethod
    def deserialize(serialized: str | dict) -> 'TechniqueContent':
        if isinstance(serialized, str): serialized = json.loads(serialized)
        return TechniqueContent(
            content_type = serialized['content_type'],
            contents = serialized['contents'],
            title = serialized.get('title', None),
            video_start = serialized.get('video_start', None))

    def serialize(self) -> dict[str, Any]:
        serialized = {
            'content_type': self.content_type,
            'contents': self.contents }
        if self.title: serialized['title'] = self.title
        if self.video_start: serialized['video_start_at'] = self.video_start
        return serialized

class Technique:
    def __init__(self,
        id: str,
        name: str,
        name_suffix_1: str,
        name_suffix_2: str,
        other_names: str,
        summary: str,
        types: list[TechniqueType],
        difficulty: TechniqueDifficulty,
        is_counter: bool,
        requires_gi: bool,
        ranking: int,
        is_searchable: bool,
        parent: str | None,
        inverse: str | None,
        followups: list[str],
        preceding: list[str],
        concepts: list[str],
        content: list[TechniqueContent]
    ):
        self.id = id
        self.name = name
        self.name_suffix_1 = name_suffix_1
        self.name_suffix_2 = name_suffix_2
        self.other_names = other_names
        self.summary = summary
        self.types = types
        self.difficulty = difficulty
        self.is_counter = is_counter
        self.requires_gi = requires_gi
        self.ranking = ranking
        self.is_searchable = is_searchable
        self.parent = parent
        self.inverse = inverse
        self.followups = followups
        self.preceding = preceding
        self.concepts = concepts
        self.content = content

    @staticmethod
    def deserialize(serialized: str | dict) -> 'Technique':
        if isinstance(serialized, str): serialized = json.loads(serialized)
        return Technique(
            id = serialized['id'],
            name = serialized['name'],
            name_suffix_1 = serialized['name_suffix_1'],
            name_suffix_2 = serialized['name_suffix_2'],
            other_names = serialized['other_names'],
            summary = serialized['summary'],
            types = serialized['types'],
            difficulty = serialized['difficulty'],
            is_counter = serialized['is_counter'],
            requires_gi = serialized['requires_gi'],
            ranking = serialized['ranking'],
            is_searchable = serialized['is_searchable'],
            parent = serialized['parent'],
            inverse = serialized['inverse'],
            followups = serialized['followups'],
            preceding = serialized['preceding'],
            concepts = serialized['concepts'],
            content = [TechniqueContent.deserialized(x) for x in serialized['content']])

    def serialize(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'name_suffix_1': self.name_suffix_1,
            'name_suffix_2': self.name_suffix_2,
            'other_names': self.other_names,
            'summary': self.summary,
            'types': self.types,
            'difficulty': self.difficulty,
            'is_counter': self.is_counter,
            'requires_gi': self.requires_gi,
            'ranking': self.ranking,
            'is_searchable': self.is_searchable,
            'parent': self.parent,
            'inverse': self.inverse,
            'followups': self.followups,
            'preceding': self.preceding,
            'concepts': self.concepts,
            'content': [x.serialize() for x in self.content] }

__all__ = ['Technique', 'TechniqueContent', 'TechniqueType', 'TechniqueDifficulty', 'TechniqueContentType']