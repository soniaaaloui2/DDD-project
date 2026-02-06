"""CandidatInfo Value Object - Regroupe toutes les informations du candidat"""

from src.domain.shared import ValueObject
from src.domain.trainer.value_objects import Email, FullName


class CandidatInfo(ValueObject):

    __slots__ = ('_full_name', '_email')

    def __init__(self, full_name: FullName, email: Email):

        object.__setattr__(self, '_full_name', full_name)
        object.__setattr__(self, '_email', email)

    @property
    def full_name(self) -> FullName:
        return self._full_name

    @property
    def email(self) -> Email:
        return self._email

    @staticmethod
    def create(
        first_name: str,
        last_name: str,
        email: str
    ) -> 'CandidatInfo':
        return CandidatInfo(
            full_name=FullName(first_name, last_name),
            email=Email(email)
        )

    def is_complete(self) -> bool:
        return (
            self._full_name is not None
            and self._email is not None
        )

    def __str__(self) -> str:
        return f"{self._full_name} ({self._email})"
