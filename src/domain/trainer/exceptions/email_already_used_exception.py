"""Exception: l'email est déjà utilisé"""

from .trainer_account_request_exception import TrainerAccountRequestException
from ..value_objects.email import Email


class EmailAlreadyUsedException(TrainerAccountRequestException):

    def __init__(self, email: Email):
        super().__init__(
            f"Email {email} is already used"
        )
        self.email = email
