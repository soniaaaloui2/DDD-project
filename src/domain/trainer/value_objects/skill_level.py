"""SkillLevel Value object - niveau de compétence"""

from enum import Enum
from src.domain.shared import ValueObject


class SkillLevel(ValueObject):
    __slots__ = ('_level',)

    class Level(Enum):
        BEGINNER = 'BEGINNER'
        INTERMEDIATE = 'INTERMEDIATE'
        EXPERT = 'EXPERT'

    def __init__(self, level: str):
        try:
            level_enum = self.Level[level.upper()]
        except KeyError:
            valid = [l.name for l in self.Level]
            raise ValueError(f"'{level}' is invalid. Must be one of {valid}")
        object.__setattr__(self, '_level', level_enum)

    @property
    def value(self) -> str:
        return self._level.value

    @staticmethod
    def beginner() -> 'SkillLevel':
        return SkillLevel('BEGINNER')

    @staticmethod
    def intermediate() -> 'SkillLevel':
        return SkillLevel('INTERMEDIATE')

    @staticmethod
    def expert() -> 'SkillLevel':
        return SkillLevel('EXPERT')

    def is_at_least(self, other: 'SkillLevel') -> bool:
        hierarchy = {
            self.Level.BEGINNER: 1,
            self.Level.INTERMEDIATE: 2,
            self.Level.EXPERT: 3,
        }
        return hierarchy[self._level] >= hierarchy[other._level]

    def __str__(self) -> str:
        return self._level.value
