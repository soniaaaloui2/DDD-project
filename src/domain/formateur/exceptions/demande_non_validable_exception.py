"""Exception: Request cannot be validated"""

from src.domain.formateur.exceptions import DemandeCompteFormateurException
from src.domain.formateur.value_objects import DemandeId, StatutDemande


class DemandeNonValidableException(DemandeCompteFormateurException):
    """
    Exception raised when trying to validate a request that cannot be validated

    Business rule: Only requests with status EN_ATTENTE_VALIDATION can be validated
    """

    def __init__(self, demande_id: DemandeId, statut_actuel: StatutDemande):
        super().__init__(
            f"La demande {demande_id} ne peut pas être validée. "
            f"Statut actuel : {statut_actuel}. "
            f"Seules les demandes EN_ATTENTE_VALIDATION peuvent être validées."
        )
        self.demande_id = demande_id
        self.statut_actuel = statut_actuel
