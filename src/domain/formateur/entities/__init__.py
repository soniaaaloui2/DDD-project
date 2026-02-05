"""Entities for Formateur domain"""

from .skill import Skill, SkillCannotDowngradeException

__all__ = ['Skill', 'SkillCannotDowngradeException']
