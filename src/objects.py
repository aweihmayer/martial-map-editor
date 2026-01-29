from enum import IntEnum
from typing import Any
import json

class ArticleDifficulty(IntEnum):
    UNIVERSAL = 0
    BEGINNER = 10
    NOVICE = 20
    INTERMEDIATE = 30
    ADVANCED = 40
    EXPERT = 50

class ArticleType(IntEnum):
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

class ArticleContentType(IntEnum):
    TEXT = 10
    YOUTUBE_VIDEO = 30
    AD = 90

class ArticleContent:
    def __init__(self,
        content_type: ArticleContentType,
        contents: str,
        title: str | None,
        video_start: int | None
    ):
        self.content_Type = content_type
        self.contents = contents
        self.title = title
        self.video_start = video_start

    @staticmethod
    def deserialize(serialized: str | dict) -> 'ArticleContent':
        if isinstance(serialized, str): serialized = json.loads(serialized)
        return ArticleContent(
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

class Article:
    def __init__(self,
        id: str,
        name: str,
        name_suffix_1: str,
        name_suffix_2: str,
        other_names: str,
        summary: str,
        types: list[ArticleType],
        difficulty: ArticleDifficulty,
        requires_gi: bool,
        ranking: int,
        parent: str | None,
        inverse: str | None,
        followups: list[str],
        counters: list[str],
        concepts: list[str],
        content: list[ArticleContent]
    ):
        self.id = id
        self.name = name
        self.name_suffix_1 = name_suffix_1
        self.name_suffix_2 = name_suffix_2
        self.other_names = other_names
        self.summary = summary
        self.types = types
        self.difficulty = difficulty
        self.requires_gi = requires_gi
        self.ranking = ranking
        self.parent = parent
        self.inverse = inverse
        self.followups = followups
        self.counters = counters
        self.concepts = concepts
        self.content = content

    @staticmethod
    def deserialize(serialized: str | dict) -> 'Article':
        if isinstance(serialized, str): serialized = json.loads(serialized)
        return Article(
            id = serialized['id'],
            name = serialized['name'],
            name_suffix_1 = serialized['name_suffix_1'],
            name_suffix_2 = serialized['name_suffix_2'],
            other_names = serialized['other_names'],
            summary = serialized['summary'],
            types = serialized['types'],
            difficulty = serialized['difficulty'],
            requires_gi = serialized['requires_gi'],
            ranking = serialized['ranking'],
            parent = serialized['parent'],
            inverse = serialized['inverse'],
            followups = serialized['followups'],
            counters = serialized['counters'],
            concepts = serialized['concepts'],
            content = [ArticleContent.deserialized(x) for x in serialized['content']])

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
            'requires_gi': self.requires_gi,
            'ranking': self.ranking,
            'parent': self.parent,
            'inverse': self.inverse,
            'followups': self.followups,
            'counters': self.counters,
            'concepts': self.concepts,
            'content': [x.serialize() for x in self.content] }

__all__ = ['Article', 'ArticleContent', 'ArticleType', 'ArticleDifficulty', 'ArticleContentType']