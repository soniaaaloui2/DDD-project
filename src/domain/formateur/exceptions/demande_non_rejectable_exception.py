"""Exception: Request cannot be rejected"""

from src.domain.formateur.exceptions import DemandeCompteFormateurException
from src.domain.formateur.value_objects import DemandeId, StatutDemande


class DemandeNonRejetableException(DemandeCompteFormateurException):
    """
    Exception raised when trying to reject a request that cannot be rejected

    Business rule: Only requests with status EN_ATTENTE_VALIDATION can be rejected
    """

    def __init__(self, demande_id: DemandeId, statut_actuel: StatutDemande):
        super().__init__(
            f"La demande {demande_id} ne peut pas être rejetée. "
            f"Statut actuel : {statut_actuel}. "
            f"Seules les demandes EN_ATTENTE_VALIDATION peuvent être rejetées."
        )
        self.demande_id = demande_id
        self.statut_actuel = statut_actuel
