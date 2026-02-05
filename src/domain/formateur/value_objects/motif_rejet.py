"""MotifRejet - Reason for rejection"""

from src.domain.shared import ValueObject


class MotifRejet(ValueObject):
    """
    MotifRejet - Rejection reason

    Characteristics:
    ✓ Immutable
    ✓ Non-empty validation
    ✓ Max length constraint
    """
    __slots__ = ('_value',)

    MIN_LENGTH = 10
    MAX_LENGTH = 500

    def __init__(self, value: str):
        normalized = value.strip()
        if not (self.MIN_LENGTH <= len(normalized) <= self.MAX_LENGTH):
            raise ValueError(
                f"Motif de rejet must be between {self.MIN_LENGTH} and {self.MAX_LENGTH} characters"
            )
        object.__setattr__(self, '_value', normalized)

    @property
    def value(self) -> str:
        return self._value

    @staticmethod
    def create(value: str) -> 'MotifRejet':
        return MotifRejet(value)

    def __str__(self) -> str:
        return self._value
