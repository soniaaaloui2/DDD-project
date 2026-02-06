"""Domaine service: Vérifier l'unicité de l'email pour les demandes de compte formateur"""

from domain.trainer.exceptions.email_already_used_exception import EmailAlreadyUsedException
from domain.trainer.value_objects import Email
from domain.trainer.repositories import TrainerAccountRequestRepositoryInterface


class VerifyEmailUniqueness:

    def __init__(
        self,
        request_repository: TrainerAccountRequestRepositoryInterface
    ):
        self._request_repository = request_repository

    def execute(self, email: Email) -> None:
        if self._request_repository.exists_by_email(email):
            raise EmailAlreadyUsedException(email)

    def is_available(self, email: Email) -> bool:
        try:
            self.execute(email)
            return True
        except EmailAlreadyUsedException:
            return False
