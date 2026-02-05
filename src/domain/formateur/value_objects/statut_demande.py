"""StatutDemande - Status of DemandeCompteFormateur"""

from enum import Enum
from src.domain.shared import ValueObject


class StatutDemande(ValueObject):
    """
    StatutDemande - State of the onboarding request

    States:
    - EN_ATTENTE_VALIDATION: Submitted, awaiting admin review
    - VALIDEE: Approved by admin
    - REJETEE: Rejected by admin

    State machine:
    EN_ATTENTE_VALIDATION → VALIDEE
    EN_ATTENTE_VALIDATION → REJETEE
    (Final states cannot transition)
    """
    __slots__ = ('_statut',)

    class Statut(Enum):
        EN_ATTENTE_VALIDATION = 'EN_ATTENTE_VALIDATION'
        VALIDEE = 'VALIDEE'
        REJETEE = 'REJETEE'

    # Transitions autorisées
    TRANSITIONS = {
        Statut.EN_ATTENTE_VALIDATION: [Statut.VALIDEE, Statut.REJETEE],
        Statut.VALIDEE: [],  # État final
        Statut.REJETEE: [],  # État final
    }

    def __init__(self, statut: str):
        try:
            statut_enum = self.Statut[statut.upper()]
        except KeyError:
            valid = [s.name for s in self.Statut]
            raise ValueError(f"'{statut}' is invalid. Must be one of {valid}")
        object.__setattr__(self, '_statut', statut_enum)

    @property
    def value(self) -> str:
        return self._statut.value

    @staticmethod
    def en_attente_validation() -> 'StatutDemande':
        """Factory: Initial state"""
        return StatutDemande('EN_ATTENTE_VALIDATION')

    @staticmethod
    def validee() -> 'StatutDemande':
        """Factory: Approved state"""
        return StatutDemande('VALIDEE')

    @staticmethod
    def rejetee() -> 'StatutDemande':
        """Factory: Rejected state"""
        return StatutDemande('REJETEE')

    def peut_etre_validee(self) -> bool:
        """Can this status transition to VALIDEE?"""
        return self.Statut.VALIDEE in self.TRANSITIONS.get(self._statut, [])

    def peut_etre_rejetee(self) -> bool:
        """Can this status transition to REJETEE?"""
        return self.Statut.REJETEE in self.TRANSITIONS.get(self._statut, [])

    def est_finale(self) -> bool:
        """Is this a final state (no more transitions)?"""
        return len(self.TRANSITIONS.get(self._statut, [])) == 0

    def equals(self, other: 'StatutDemande') -> bool:
        """Explicit equality check (for readability in business logic)"""
        return self == other

    def __str__(self) -> str:
        return self._statut.value
