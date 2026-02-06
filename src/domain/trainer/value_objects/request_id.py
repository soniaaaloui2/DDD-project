"""RequestId Value object - identifiant pour la demande"""

import uuid
from domain.shared import ValueObject


class RequestId(ValueObject):

    __slots__ = ('_value',)

    def __init__(self, value: str):
        try:
            uuid_obj = uuid.UUID(value, version=4)
        except (ValueError, AttributeError):
            raise ValueError(f"'{value}' is not a valid UUID")
        object.__setattr__(self, '_value', str(uuid_obj).lower())

    @property
    def value(self) -> str:
        return self._value

    @staticmethod
    def generate() -> 'RequestId':
        return RequestId(str(uuid.uuid4()))

    @staticmethod
    def from_string(value: str) -> 'RequestId':
        return RequestId(value)

    def __str__(self) -> str:
        return self._value
