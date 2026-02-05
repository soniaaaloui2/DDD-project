"""DemandeId - Unique identifier for DemandeCompteFormateur"""

import uuid
from src.domain.shared import ValueObject


class DemandeId(ValueObject):

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
    def generate() -> 'DemandeId':
        """Generate a new unique DemandeId"""
        return DemandeId(str(uuid.uuid4()))

    @staticmethod
    def from_string(value: str) -> 'DemandeId':
        """Reconstruct DemandeId from string"""
        return DemandeId(value)

    def __str__(self) -> str:
        return self._value
