"""Interface Repository pour l'agrégat du formateur"""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.trainer.value_objects import RequestId, Email, RequestStatus
from src.domain.trainer.aggregates import TrainerAccountRequest


class TrainerAccountRequestRepositoryInterface(ABC):

    @abstractmethod
    def save(self, request: TrainerAccountRequest) -> None:
        pass

    @abstractmethod
    def find(self, request_id: RequestId) -> Optional[TrainerAccountRequest]:
        pass

    @abstractmethod
    def find_by_email(self, email: Email) -> Optional[TrainerAccountRequest]:
        pass

    @abstractmethod
    def find_pending_validation(self) -> List[TrainerAccountRequest]:
        pass

    @abstractmethod
    def find_by_status(self, status: RequestStatus) -> List[TrainerAccountRequest]:
        pass

    @abstractmethod
    def exists_by_email(self, email: Email) -> bool:
        pass

    @abstractmethod
    def delete(self, request: TrainerAccountRequest) -> None:
        pass

