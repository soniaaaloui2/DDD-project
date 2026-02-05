"""SkillId - Unique identifier for Skill (local to Formateur)"""

import uuid
from src.domain.shared import ValueObject


class SkillId(ValueObject):
    __slots__ = ('_value',)

    def __init__(self, value: str):
        try:
            uuid_obj = uuid.UUID(value, version=4)
        except (ValueError, AttributeError):
            raise ValueError(f"'{value}' is not a valid UUID v4")
        object.__setattr__(self, '_value', str(uuid_obj).lower())

    @property
    def value(self) -> str:
        return self._value

    @staticmethod
    def generate() -> 'SkillId':
        return SkillId(str(uuid.uuid4()))

    def __str__(self) -> str:
        return self._value
