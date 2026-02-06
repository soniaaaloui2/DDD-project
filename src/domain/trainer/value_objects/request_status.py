"""RequestStatus Value object - status de la demande"""

from enum import Enum
from domain.shared import ValueObject


class RequestStatus(ValueObject):

    __slots__ = ('_status',)

    class Status(Enum):
        PENDING_VALIDATION = 'PENDING_VALIDATION'
        APPROVED = 'APPROVED'
        REJECTED = 'REJECTED'

    TRANSITIONS = {
        Status.PENDING_VALIDATION: [Status.APPROVED, Status.REJECTED],
        Status.APPROVED: [],
        Status.REJECTED: [],
    }

    def __init__(self, status: str):
        try:
            status_enum = self.Status[status.upper()]
        except KeyError:
            valid = [s.name for s in self.Status]
            raise ValueError(f"'{status}' is invalid. Must be one of {valid}")
        object.__setattr__(self, '_status', status_enum)

    @property
    def value(self) -> str:
        return self._status.value

    @staticmethod
    def pending_validation() -> 'RequestStatus':
        return RequestStatus('PENDING_VALIDATION')

    @staticmethod
    def approved() -> 'RequestStatus':
        return RequestStatus('APPROVED')

    @staticmethod
    def rejected() -> 'RequestStatus':
        return RequestStatus('REJECTED')

    def can_be_approved(self) -> bool:
        return self.Status.APPROVED in self.TRANSITIONS.get(self._status, [])

    def can_be_rejected(self) -> bool:
        return self.Status.REJECTED in self.TRANSITIONS.get(self._status, [])

    def is_final(self) -> bool:
        return len(self.TRANSITIONS.get(self._status, [])) == 0

    def equals(self, other: 'RequestStatus') -> bool:
        return self == other

    def __str__(self) -> str:
        return self._status.value
