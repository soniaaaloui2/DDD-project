"""Tests pour l'entité Skill du domaine Formateur"""

import sys
from pathlib import Path

src_path = Path(__file__).parent.parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from domain.trainer import (
    Skill,
    SkillName,
    SkillLevel,
    SkillId,
    SkillCannotDowngradeException,
)


def test_skill_creation():
    skill = Skill.create(SkillName('Python'), SkillLevel('BEGINNER'))

    assert skill.name == SkillName('Python')
    assert skill.level == SkillLevel('BEGINNER')
    assert skill.id

    print("Skill creation tests passed")


def test_skill_identity():
    skill1 = Skill.create(SkillName('Python'), SkillLevel('BEGINNER'))
    skill2 = Skill.create(SkillName('Python'), SkillLevel('BEGINNER'))

    assert skill1.name == skill2.name
    assert skill1.level == skill2.level
    assert skill1 != skill2
    assert skill1.id != skill2.id

    print("Skill identity tests passed")


def test_skill_upgrade_level():
    skill = Skill.create(SkillName('Python'), SkillLevel('BEGINNER'))

    skill.upgrade_level(SkillLevel('INTERMEDIATE'))
    assert skill.level == SkillLevel('INTERMEDIATE')

    skill.upgrade_level(SkillLevel('EXPERT'))
    assert skill.level == SkillLevel('EXPERT')

    print("Skill upgrade tests passed")


def test_skill_cannot_downgrade():
    skill = Skill.create(SkillName('Python'), SkillLevel('INTERMEDIATE'))

    try:
        skill.upgrade_level(SkillLevel('BEGINNER'))
        assert False, "Should have raised exception"
    except SkillCannotDowngradeException as e:
        assert 'downgrade' in str(e).lower()

    print("Skill cannot downgrade tests passed")


def test_skill_same_level():
    skill = Skill.create(SkillName('Python'), SkillLevel('EXPERT'))

    skill.upgrade_level(SkillLevel('EXPERT'))
    assert skill.level == SkillLevel('EXPERT')

    print("Skill same level tests passed")


def test_skill_immutable_name():
    skill = Skill.create(SkillName('Python'), SkillLevel('BEGINNER'))

    original_name = skill.name
    assert skill.name == original_name

    print("Skill immutable name tests passed")


def test_skill_equality_by_identity():
    skill_id = SkillId.generate()
    skill1 = Skill(skill_id, SkillName('Python'), SkillLevel('BEGINNER'))
    skill2 = Skill(skill_id, SkillName('Python'), SkillLevel('BEGINNER'))

    assert skill1 == skill2

    skill3 = Skill(SkillId.generate(), SkillName('Python'), SkillLevel('BEGINNER'))
    assert skill1 != skill3

    print("Skill equality by identity tests passed")


if __name__ == '__main__':
    test_skill_creation()
    test_skill_identity()
    test_skill_upgrade_level()
    test_skill_cannot_downgrade()
    test_skill_same_level()
    test_skill_immutable_name()
    test_skill_equality_by_identity()
    print("\nAll Skill entity tests passed!")
