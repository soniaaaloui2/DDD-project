"""Event: DemandeCompteFormateur has been submitted"""

from datetime import datetime
from src.domain.formateur.value_objects import DemandeId, Email


class DemandeCompteFormateurSoumise:
    """
    Domain Event: A trainer account request has been submitted

    Characteristics (from course):
    ✓ Named in past tense (Soumise, not Soumettre)
    ✓ Immutable (readonly attributes)
    ✓ Factual (describes what happened)
    ✓ Ubiquitous Language (business vocabulary)

    When raised:
    - After a candidate submits their request

    Listeners might:
    - Send confirmation email to candidate
    - Notify admins
    - Log the event
    """

    def __init__(
        self,
        demande_id: DemandeId,
        candidat_email: Email,
        occurred_on: datetime = None
    ):
        """
        Create domain event.

        Args:
            demande_id: ID of the submitted request
            candidat_email: Email of the candidate
            occurred_on: When the event occurred (defaults to now)
        """
        self.demande_id = demande_id
        self.candidat_email = candidat_email
        self.occurred_on = occurred_on or datetime.now()

    def __repr__(self) -> str:
        return (
            f"DemandeCompteFormateurSoumise("
            f"demande_id={self.demande_id}, "
            f"candidat_email={self.candidat_email}, "
            f"occurred_on={self.occurred_on})"
        )
