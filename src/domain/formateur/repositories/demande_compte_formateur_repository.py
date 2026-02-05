"""Repository interface for DemandeCompteFormateur aggregate"""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.formateur.value_objects import DemandeId, Email, StatutDemande
from src.domain.formateur.aggregates import DemandeCompteFormateur


class DemandeCompteFormateurRepositoryInterface(ABC):
    """
    Repository for DemandeCompteFormateur Aggregate Root

    Principles (from DDD course):
    ✓ Interface in Domain layer (infrastructure-agnostic)
    ✓ One repository per Aggregate Root
    ✓ Saves/loads the ENTIRE aggregate (including Skills)
    ✓ Method names use business vocabulary

    This is an INTERFACE (Abstract Base Class).
    The actual implementation (Doctrine, SQLAlchemy, etc.)
    will be in the Infrastructure layer.

    Why an interface?
    - Domain doesn't depend on infrastructure
    - Easy to swap implementations (SQL → NoSQL → in-memory)
    - Testable with fake implementations
    """

    @abstractmethod
    def save(self, demande: DemandeCompteFormateur) -> None:
        """
        Save the entire aggregate (insert or update).

        Persists:
        - DemandeCompteFormateur (root)
        - All Skills (internal entities)
        - All value objects

        Args:
            demande: The aggregate to save

        Implementation notes:
        - Should publish domain events after saving
        - Should handle both insert and update
        """
        pass

    @abstractmethod
    def find(self, demande_id: DemandeId) -> Optional[DemandeCompteFormateur]:
        """
        Find a demande by its ID.

        Loads the ENTIRE aggregate (including all skills).

        Args:
            demande_id: Unique identifier

        Returns:
            The aggregate if found, None otherwise
        """
        pass

    @abstractmethod
    def find_by_email(self, email: Email) -> Optional[DemandeCompteFormateur]:
        """
        Find a demande by candidate email.

        Business use case: Check if email already has a pending request.

        Args:
            email: Candidate email

        Returns:
            The aggregate if found, None otherwise
        """
        pass

    @abstractmethod
    def find_en_attente_validation(self) -> List[DemandeCompteFormateur]:
        """
        Find all requests awaiting validation.

        Business use case: Admin dashboard showing pending requests.

        Returns:
            List of demandes with status EN_ATTENTE_VALIDATION
        """
        pass

    @abstractmethod
    def find_by_statut(self, statut: StatutDemande) -> List[DemandeCompteFormateur]:
        """
        Find all requests with a specific status.

        Args:
            statut: The status to filter by

        Returns:
            List of demandes with the given status
        """
        pass

    @abstractmethod
    def exists_by_email(self, email: Email) -> bool:
        """
        Check if a demande exists for this email.

        Business use case: Validate email uniqueness before submission.
        More efficient than find_by_email when you only need existence.

        Args:
            email: Candidate email

        Returns:
            True if a demande exists, False otherwise
        """
        pass

    @abstractmethod
    def delete(self, demande: DemandeCompteFormateur) -> None:
        """
        Delete an aggregate.

        Deletes:
        - DemandeCompteFormateur (root)
        - All Skills (cascade delete)

        Args:
            demande: The aggregate to delete
        """
        pass

    @abstractmethod
    def count_by_statut(self, statut: StatutDemande) -> int:
        """
        Count demandes by status.

        Business use case: Dashboard statistics.

        Args:
            statut: The status to count

        Returns:
            Number of demandes with this status
        """
        pass
