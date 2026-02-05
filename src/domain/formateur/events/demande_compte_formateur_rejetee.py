"""Event: DemandeCompteFormateur has been rejected"""

from datetime import datetime
from src.domain.formateur.value_objects import DemandeId, FormateurId, MotifRejet


class DemandeCompteFormateurRejetee:
    """
    Domain Event: A trainer account request has been rejected by an admin

    When raised:
    - After an admin rejects the request

    Listeners might:
    - Send rejection email with reason
    - Log the rejection
    - Archive the request
    """

    def __init__(
        self,
        demande_id: DemandeId,
        rejete_par_admin_id: FormateurId,
        motif: MotifRejet,
        occurred_on: datetime = None
    ):
        """
        Create domain event.

        Args:
            demande_id: ID of the rejected request
            rejete_par_admin_id: ID of the admin who rejected
            motif: Reason for rejection
            occurred_on: When the event occurred
        """
        self.demande_id = demande_id
        self.rejete_par_admin_id = rejete_par_admin_id
        self.motif = motif
        self.occurred_on = occurred_on or datetime.now()

    def __repr__(self) -> str:
        return (
            f"DemandeCompteFormateurRejetee("
            f"demande_id={self.demande_id}, "
            f"rejete_par={self.rejete_par_admin_id}, "
            f"motif={self.motif}, "
            f"occurred_on={self.occurred_on})"
        )
