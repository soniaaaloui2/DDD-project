"""FullName - Composite value object"""

from src.domain.shared import ValueObject


class FullName(ValueObject):
    __slots__ = ('_first_name', '_last_name')

    MIN_LENGTH = 2
    MAX_LENGTH = 100

    def __init__(self, first_name: str, last_name: str):
        first_name_normalized = self._normalize(first_name)
        last_name_normalized = self._normalize(last_name)

        if not self._is_valid_name(first_name_normalized):
            raise ValueError(f"First name '{first_name}' is invalid")
        if not self._is_valid_name(last_name_normalized):
            raise ValueError(f"Last name '{last_name}' is invalid")

        object.__setattr__(self, '_first_name', first_name_normalized)
        object.__setattr__(self, '_last_name', last_name_normalized)

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"

    @staticmethod
    def create(first_name: str, last_name: str) -> 'FullName':
        return FullName(first_name, last_name)

    def __str__(self) -> str:
        return self.full_name()

    @staticmethod
    def _normalize(name: str) -> str:
        trimmed = name.strip()
        return trimmed.capitalize()

    @staticmethod
    def _is_valid_name(name: str) -> bool:
        if not (FullName.MIN_LENGTH <= len(name) <= FullName.MAX_LENGTH):
            return False
        return all(c.isalpha() or c in "-' " for c in name)
