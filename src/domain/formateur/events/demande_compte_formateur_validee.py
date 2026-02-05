"""Event: DemandeCompteFormateur has been validated"""

from datetime import datetime
from src.domain.formateur.value_objects import DemandeId, FormateurId


class DemandeCompteFormateurValidee:
    """
    Domain Event: A trainer account request has been validated by an admin

    When raised:
    - After an admin approves the request

    Listeners might:
    - Create the CompteFormateur
    - Send welcome email
    - Generate access credentials
    - Notify the candidate
    """

    def __init__(
        self,
        demande_id: DemandeId,
        valide_par_admin_id: FormateurId,  # L'admin qui a validé
        occurred_on: datetime = None
    ):
        """
        Create domain event.

        Args:
            demande_id: ID of the validated request
            valide_par_admin_id: ID of the admin who validated
            occurred_on: When the event occurred
        """
        self.demande_id = demande_id
        self.valide_par_admin_id = valide_par_admin_id
        self.occurred_on = occurred_on or datetime.now()

    def __repr__(self) -> str:
        return (
            f"DemandeCompteFormateurValidee("
            f"demande_id={self.demande_id}, "
            f"valide_par={self.valide_par_admin_id}, "
            f"occurred_on={self.occurred_on})"
        )
