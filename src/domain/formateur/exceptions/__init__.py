"""Domain Exceptions for Formateur domain"""

from .demande_compte_formateur_exception import DemandeCompteFormateurException
from .competences_requises_exception import CompetencesRequisesException
from .demande_non_validable_exception import DemandeNonValidableException
from .demande_non_rejectable_exception import DemandeNonRejetableException
from .motif_rejet_obligatoire_exception import MotifRejetObligatoireException
from .email_deja_utilise_exception import EmailDejaUtiliseException

__all__ = [
    'DemandeCompteFormateurException',
    'CompetencesRequisesException',
    'DemandeNonValidableException',
    'DemandeNonRejetableException',
    'MotifRejetObligatoireException',
    'EmailDejaUtiliseException',
]
