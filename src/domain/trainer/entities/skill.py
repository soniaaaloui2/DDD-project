"""Skill Entity - Compétences d'un formateur"""

from src.domain.shared import Entity
from src.domain.trainer.value_objects import SkillId, SkillName, SkillLevel
from src.domain.trainer.exceptions import SkillCannotDowngradeException


class Skill(Entity[SkillId]):

    def __init__(self, skill_id: SkillId, name: SkillName, level: SkillLevel):

        super().__init__(skill_id)
        self._name = name
        self._level = level

    @property
    def name(self) -> SkillName:
        return self._name

    @property
    def level(self) -> SkillLevel:
        return self._level

    def upgrade_level(self, new_level: SkillLevel) -> None:
        if not new_level.is_at_least(self._level):
            raise SkillCannotDowngradeException(
                f"Cannot downgrade skill '{self._name}' from {self._level} to {new_level}"
            )
        self._level = new_level

    @staticmethod
    def create(name: SkillName, level: SkillLevel) -> 'Skill':
        return Skill(SkillId.generate(), name, level)

    def __repr__(self) -> str:
        return f"Skill(id={self._id!r}, name={self._name!r}, level={self._level!r})"
