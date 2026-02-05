"""Email - Validated and normalized email value object"""

import re
from src.domain.shared import ValueObject


class Email(ValueObject):
    __slots__ = ('_value',)

    MIN_LENGTH = 5
    MAX_LENGTH = 254
    EMAIL_PATTERN = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]+$')

    def __init__(self, value: str):
        normalized = self._normalize(value)
        if not self._is_valid(normalized):
            raise ValueError(f"'{value}' is not a valid email address")
        object.__setattr__(self, '_value', normalized)

    @property
    def value(self) -> str:
        return self._value

    @staticmethod
    def create(value: str) -> 'Email':
        return Email(value)

    def __str__(self) -> str:
        return self._value

    @staticmethod
    def _normalize(email: str) -> str:
        return email.strip().lower()

    @staticmethod
    def _is_valid(email: str) -> bool:
        if not (Email.MIN_LENGTH <= len(email) <= Email.MAX_LENGTH):
            return False
        return bool(Email.EMAIL_PATTERN.match(email))
