"""Entities pour le domaine Formateur"""

from .skill import Skill
from src.domain.trainer.exceptions import SkillCannotDowngradeException

__all__ = ['Skill', 'SkillCannotDowngradeException']
