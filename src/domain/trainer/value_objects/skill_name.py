"""SkillName Value object - Nom de la compétence"""

from src.domain.shared import ValueObject


class SkillName(ValueObject):
    __slots__ = ('_value',)

    MIN_LENGTH = 2
    MAX_LENGTH = 100

    def __init__(self, value: str):
        normalized = value.strip().capitalize()
        if not (self.MIN_LENGTH <= len(normalized) <= self.MAX_LENGTH):
            raise ValueError(
                f"Skill name '{value}' must be between {self.MIN_LENGTH} and {self.MAX_LENGTH} characters"
            )
        object.__setattr__(self, '_value', normalized)

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value
