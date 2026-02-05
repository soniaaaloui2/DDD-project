"""Formateur domain - Bounded Context"""

from .value_objects import (
    FormateurId,
    Email,
    FullName,
    CandidatInfo,
    SkillId,
    SkillName,
    SkillLevel,
    OnboardingStatus,
    DemandeId,
    StatutDemande,
    MotifRejet,
)

from .entities import (
    Skill,
    SkillCannotDowngradeException,
)

from .aggregates import (
    DemandeCompteFormateur,
)

from .events import (
    DemandeCompteFormateurSoumise,
    DemandeCompteFormateurValidee,
    DemandeCompteFormateurRejetee,
)

from .exceptions import (
    DemandeCompteFormateurException,
    CompetencesRequisesException,
    DemandeNonValidableException,
    DemandeNonRejetableException,
    MotifRejetObligatoireException,
)

__all__ = [
    # Value Objects
    'FormateurId',
    'Email',
    'FullName',
    'CandidatInfo',
    'SkillId',
    'SkillName',
    'SkillLevel',
    'OnboardingStatus',
    'DemandeId',
    'StatutDemande',
    'MotifRejet',
    # Entities
    'Skill',
    'SkillCannotDowngradeException',
    # Aggregates
    'DemandeCompteFormateur',
    # Events
    'DemandeCompteFormateurSoumise',
    'DemandeCompteFormateurValidee',
    'DemandeCompteFormateurRejetee',
    # Exceptions
    'DemandeCompteFormateurException',
    'CompetencesRequisesException',
    'DemandeNonValidableException',
    'DemandeNonRejetableException',
    'MotifRejetObligatoireException',
]
