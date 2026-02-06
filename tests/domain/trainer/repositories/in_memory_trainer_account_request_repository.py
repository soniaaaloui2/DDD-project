"""Données d'entrée pour les tests du repository de demandes de compte formateur"""

from typing import List, Optional, Dict
import sys
from pathlib import Path

from src.domain.trainer.aggregates.trainer_account_request import TrainerAccountRequest

project_root = Path(__file__).parent.parent.parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(project_root))

from domain.trainer.value_objects import RequestId, Email, RequestStatus
from domain.trainer.repositories import TrainerAccountRequestRepositoryInterface


class InMemoryTrainerAccountRequestRepository(TrainerAccountRequestRepositoryInterface):

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
        for request in self._requests.values():
            if request.candidate_info.email == email:
                return request
        return None

    def find_pending_validation(self) -> List[TrainerAccountRequest]:
        return [
            request for request in self._requests.values()
            if request.statut == RequestStatus.pending_validation()
        ]

    def find_by_status(self, status: RequestStatus) -> List[TrainerAccountRequest]:
        return [
            request for request in self._requests.values()
            if request.statut == status
        ]

    def exists_by_email(self, email: Email) -> bool:
        return self.find_by_email(email) is not None

    def delete(self, request: TrainerAccountRequest) -> None:
        if request.id.value in self._requests:
            del self._requests[request.id.value]

    def count_by_status(self, status: RequestStatus) -> int:
        return len(self.find_by_status(status))

    def count_all(self) -> int:
        return len(self._requests)

    def clear(self) -> None:
        self._requests.clear()
