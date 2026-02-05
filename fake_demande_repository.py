"""Fake in-memory repository for testing"""

from typing import List, Optional, Dict

from src.domain.formateur.value_objects import DemandeId, Email, StatutDemande
from src.domain.formateur.aggregates import DemandeCompteFormateur
from src.domain.formateur.repositories import DemandeCompteFormateurRepositoryInterface


class FakeDemandeCompteFormateurRepository(DemandeCompteFormateurRepositoryInterface):
    """
    In-memory fake repository for testing.

    Stores aggregates in a dictionary.
    No database, no persistence between test runs.

    Perfect for:
    - Unit tests
    - Integration tests without database
    - Fast tests
    """

    def __init__(self):
        """Initialize empty storage"""
        self._demandes: Dict[str, DemandeCompteFormateur] = {}

    def save(self, demande: DemandeCompteFormateur) -> None:
        """Save in memory"""
        self._demandes[demande.id.value] = demande

    def find(self, demande_id: DemandeId) -> Optional[DemandeCompteFormateur]:
        """Find by ID"""
        return self._demandes.get(demande_id.value)

    def find_by_email(self, email: Email) -> Optional[DemandeCompteFormateur]:
        """Find by email"""
        for demande in self._demandes.values():
            if demande.candidat_info.email == email:
                return demande
        return None

    def find_en_attente_validation(self) -> List[DemandeCompteFormateur]:
        """Find all pending requests"""
        return [
            demande for demande in self._demandes.values()
            if demande.statut == StatutDemande.en_attente_validation()
        ]

    def find_by_statut(self, statut: StatutDemande) -> List[DemandeCompteFormateur]:
        """Find by status"""
        return [
            demande for demande in self._demandes.values()
            if demande.statut == statut
        ]

    def exists_by_email(self, email: Email) -> bool:
        """Check if email exists"""
        return self.find_by_email(email) is not None

    def delete(self, demande: DemandeCompteFormateur) -> None:
        """Delete from memory"""
        if demande.id.value in self._demandes:
            del self._demandes[demande.id.value]

    def count_by_statut(self, statut: StatutDemande) -> int:
        """Count by status"""
        return len(self.find_by_statut(statut))

    # Helper methods for testing
    def clear(self) -> None:
        """Clear all data (useful between tests)"""
        self._demandes.clear()

    def count_all(self) -> int:
        """Count all demandes"""
        return len(self._demandes)
