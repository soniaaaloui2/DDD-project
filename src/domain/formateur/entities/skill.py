"""Skill - Internal entity within Formateur aggregate"""

from src.domain.shared import Entity
from src.domain.formateur.value_objects import SkillId, SkillName, SkillLevel


class SkillCannotDowngradeException(Exception):
    """Cannot downgrade a skill level"""
    pass


class Skill(Entity[SkillId]):
    """
    Skill - Internal Entity
    
    Characteristics:
    ✓ Has local identity (SkillId - unique within Formateur)
    ✓ Mutable - Can change state (level can be upgraded)
    ✓ Equality by identity (not by value)
    ✓ Lifecycle tied to Formateur (cannot exist independently)
    
    Rules:
    - Level can only be upgraded, never downgraded
    - Name is immutable after creation
    """

    def __init__(self, skill_id: SkillId, name: SkillName, level: SkillLevel):
        """
        Create a Skill entity.
        
        Args:
            skill_id: Local unique identifier
            name: Skill name (immutable)
            level: Current skill level (can be upgraded)
        """
        super().__init__(skill_id)
        self._name = name
        self._level = level

    @property
    def name(self) -> SkillName:
        """Get skill name (immutable)"""
        return self._name

    @property
    def level(self) -> SkillLevel:
        """Get current skill level"""
        return self._level

    def upgrade_level(self, new_level: SkillLevel) -> None:
        """
        Upgrade skill level.
        
        Business rule: Can only upgrade, never downgrade.
        
        Args:
            new_level: New skill level
            
        Raises:
            SkillCannotDowngradeException: If trying to downgrade
        """
        if not new_level.is_at_least(self._level):
            raise SkillCannotDowngradeException(
                f"Cannot downgrade skill '{self._name}' from {self._level} to {new_level}"
            )
        self._level = new_level

    @staticmethod
    def create(name: SkillName, level: SkillLevel) -> 'Skill':
        """
        Factory method to create a new Skill.
        
        Args:
            name: Skill name
            level: Initial skill level
            
        Returns:
            New Skill entity with generated ID
        """
        return Skill(SkillId.generate(), name, level)

    def __repr__(self) -> str:
        return f"Skill(id={self._id!r}, name={self._name!r}, level={self._level!r})"
