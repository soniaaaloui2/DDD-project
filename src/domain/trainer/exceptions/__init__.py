"""Expections pour le domaine Formateur"""

from .trainer_account_request_exception import TrainerAccountRequestException
from .required_skills_exception import RequiredSkillsException
from .email_already_used_exception import EmailAlreadyUsedException
from .skill_cannot_downgrade_exception import SkillCannotDowngradeException

__all__ = [
    'TrainerAccountRequestException',
    'RequiredSkillsException',
    'EmailAlreadyUsedException',
    'SkillCannotDowngradeException',
]
