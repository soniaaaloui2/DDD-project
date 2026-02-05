"""Exception: Rejection reason is required"""

from src.domain.formateur.exceptions import DemandeCompteFormateurException


class MotifRejetObligatoireException(DemandeCompteFormateurException):
    """
    Exception raised when trying to reject without providing a reason

    Business rule: A rejection reason must be provided
    """

    def __init__(self):
        super().__init__(
            "Un motif de rejet est obligatoire pour rejeter une demande"
        )
