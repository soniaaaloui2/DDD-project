"""Exception: At least one skill is required"""

from src.domain.formateur.exceptions import DemandeCompteFormateurException


class CompetencesRequisesException(DemandeCompteFormateurException):
    """
    Exception raised when trying to submit a request without skills

    Business rule: A trainer must have at least one skill
    """

    def __init__(self):
        super().__init__(
            "Au moins une compétence est requise pour soumettre une demande de compte formateur"
        )
