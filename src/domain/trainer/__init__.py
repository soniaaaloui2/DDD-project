"""Domaine Formateur - Bounded Context"""

from .value_objects import (
    Email,
    FullName,
    CandidatInfo,
    SkillId,
    SkillName,
    SkillLevel,
    RequestId,
    RequestStatus,
)

from .entities import (
    Skill,
)

from .aggregates import (
    TrainerAccountRequest,
)

from .events import (
    TrainerAccountRequestSubmitted,
)

from .exceptions import (
    TrainerAccountRequestException,
    RequiredSkillsException,
    EmailAlreadyUsedException,
    SkillCannotDowngradeException,
)

from .repositories import (
    TrainerAccountRequestRepositoryInterface,
)

from .services import (
    VerifyEmailUniqueness,
)

__all__ = [
    # Value Objects
    'Email',
    'FullName',
    'CandidatInfo',
    'SkillId',
    'SkillName',
    'SkillLevel',
    'RequestId',
    'RequestStatus',
    # Entities
    'Skill',
    # Aggregates
    'TrainerAccountRequest',
    # Events
    'TrainerAccountRequestSubmitted',
    # Exceptions
    'TrainerAccountRequestException',
    'RequiredSkillsException',
    'EmailAlreadyUsedException',
    'SkillCannotDowngradeException',
    # Repositories
    'TrainerAccountRequestRepositoryInterface',
    # Services
    'VerifyEmailUniqueness',
]
