"""Fake in-memory repository for testing"""

from typing import List, Optional, Dict

from src.domain.trainer.value_objects import RequestId, Email, RequestStatus
from src.domain.trainer.aggregates import TrainerAccountRequest
from src.domain.trainer.repositories import TrainerAccountRequestRepositoryInterface


class FakeTrainerAccountRequestRepository(TrainerAccountRequestRepositoryInterface):
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
        self._requests: Dict[str, TrainerAccountRequest] = {}

    def save(self, request: TrainerAccountRequest) -> None:
        """Save in memory"""
        self._requests[request.id.value] = request

    def find(self, request_id: RequestId) -> Optional[TrainerAccountRequest]:
        """Find by ID"""
        return self._requests.get(request_id.value)

    def find_by_email(self, email: Email) -> Optional[TrainerAccountRequest]:
        """Find by email"""
        for request in self._requests.values():
            if request.candidate_info.email == email:
                return request
        return None

    def find_pending_validation(self) -> List[TrainerAccountRequest]:
        """Find all pending requests"""
        return [
            request for request in self._requests.values()
            if request.statut == RequestStatus.pending_validation()
        ]

    def find_by_status(self, status: RequestStatus) -> List[TrainerAccountRequest]:
        """Find by status"""
        return [
            request for request in self._requests.values()
            if request.statut == status
        ]

    def exists_by_email(self, email: Email) -> bool:
        """Check if email exists"""
        return self.find_by_email(email) is not None

    def delete(self, request: TrainerAccountRequest) -> None:
        """Delete from memory"""
        if request.id.value in self._requests:
            del self._requests[request.id.value]

    def count_by_status(self, status: RequestStatus) -> int:
        """Count by status"""
        return len(self.find_by_status(status))

    # Helper methods for testing
    def clear(self) -> None:
        """Clear all data (useful between tests)"""
        self._requests.clear()

    def count_all(self) -> int:
        """Count all requests"""
        return len(self._requests)

    # Backwards compatibility methods (old names)
    def find_by_statut(self, statut: RequestStatus) -> List[TrainerAccountRequest]:
        """Backwards compatibility wrapper for find_by_status"""
        return self.find_by_status(statut)

    def count_by_statut(self, statut: RequestStatus) -> int:
        """Backwards compatibility wrapper for count_by_status"""
        return self.count_by_status(statut)


# Backwards compatibility alias
FakeDemandeCompteFormateurRepository = FakeTrainerAccountRequestRepository
