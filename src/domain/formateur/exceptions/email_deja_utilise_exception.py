"""Exception: Email already used in an existing request"""

from .demande_compte_formateur_exception import DemandeCompteFormateurException
from ..value_objects.email import Email


class EmailDejaUtiliseException(DemandeCompteFormateurException):
    """
    Exception raised when email is already used in an existing request.

    Business rule: An email can only have one active request.
    """

    def __init__(self, email: Email):
        super().__init__(
            f"L'email {email} est déjà utilisé dans une demande existante"
        )
        self.email = email
