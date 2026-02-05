"""OnboardingStatus - State of the onboarding process"""

from enum import Enum
from src.domain.shared import ValueObject


class OnboardingStatus(ValueObject):
    __slots__ = ('_status',)

    class Status(Enum):
        STARTED = 'STARTED'
        SKILLS_COMPLETED = 'SKILLS_COMPLETED'
        ACCOUNT_REQUESTED = 'ACCOUNT_REQUESTED'

    TRANSITIONS = {
        Status.STARTED: [Status.SKILLS_COMPLETED],
        Status.SKILLS_COMPLETED: [Status.ACCOUNT_REQUESTED],
        Status.ACCOUNT_REQUESTED: [],
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
    def initial() -> 'OnboardingStatus':
        return OnboardingStatus('STARTED')

    def can_transition_to(self, new_status: 'OnboardingStatus') -> bool:
        allowed = self.TRANSITIONS.get(self._status, [])
        return new_status._status in allowed

    def is_at_least(self, status: str) -> bool:
        hierarchy = {
            self.Status.STARTED: 1,
            self.Status.SKILLS_COMPLETED: 2,
            self.Status.ACCOUNT_REQUESTED: 3,
        }
        try:
            target_status = self.Status[status.upper()]
        except KeyError:
            return False
        return hierarchy[self._status] >= hierarchy[target_status]

    def __str__(self) -> str:
        return self._status.value
