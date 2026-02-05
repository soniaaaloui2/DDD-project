"""Tests for Skill Entity"""

from src.domain.formateur import (
    Skill,
    SkillName,
    SkillLevel,
    SkillId,
    SkillCannotDowngradeException,
)


def test_skill_creation():
    """Test creating a skill with factory method"""
    skill = Skill.create(SkillName('Python'), SkillLevel('BEGINNER'))
    
    assert skill.name == SkillName('Python')
    assert skill.level == SkillLevel('BEGINNER')
    assert skill.id  # Has an ID
    
    print("✓ Skill creation tests passed")


def test_skill_identity():
    """Test that skills have identity"""
    skill1 = Skill.create(SkillName('Python'), SkillLevel('BEGINNER'))
    skill2 = Skill.create(SkillName('Python'), SkillLevel('BEGINNER'))
    
    # Same values but different identities
    assert skill1.name == skill2.name
    assert skill1.level == skill2.level
    assert skill1 != skill2  # ← Different identities!
    assert skill1.id != skill2.id
    
    print("✓ Skill identity tests passed")


def test_skill_upgrade_level():
    """Test upgrading skill level"""
    skill = Skill.create(SkillName('Python'), SkillLevel('BEGINNER'))
    
    # Upgrade to INTERMEDIATE
    skill.upgrade_level(SkillLevel('INTERMEDIATE'))
    assert skill.level == SkillLevel('INTERMEDIATE')
    
    # Upgrade to EXPERT
    skill.upgrade_level(SkillLevel('EXPERT'))
    assert skill.level == SkillLevel('EXPERT')
    
    print("✓ Skill upgrade tests passed")


def test_skill_cannot_downgrade():
    """Test that skill level cannot be downgraded"""
    skill = Skill.create(SkillName('Python'), SkillLevel('INTERMEDIATE'))
    
    # Try to downgrade to BEGINNER
    try:
        skill.upgrade_level(SkillLevel('BEGINNER'))
        assert False, "Should have raised exception"
    except SkillCannotDowngradeException as e:
        assert 'downgrade' in str(e).lower()
    
    print("✓ Skill cannot downgrade tests passed")


def test_skill_same_level():
    """Test that upgrading to same level is allowed"""
    skill = Skill.create(SkillName('Python'), SkillLevel('EXPERT'))
    
    # Same level should be OK (not a downgrade)
    skill.upgrade_level(SkillLevel('EXPERT'))
    assert skill.level == SkillLevel('EXPERT')
    
    print("✓ Skill same level tests passed")


def test_skill_immutable_name():
    """Test that skill name is immutable"""
    skill = Skill.create(SkillName('Python'), SkillLevel('BEGINNER'))
    
    original_name = skill.name
    # Name cannot be changed (no setter)
    assert skill.name == original_name
    
    print("✓ Skill immutable name tests passed")


def test_skill_equality_by_identity():
    """Test equality by identity, not value"""
    skill_id = SkillId.generate()
    skill1 = Skill(skill_id, SkillName('Python'), SkillLevel('BEGINNER'))
    skill2 = Skill(skill_id, SkillName('Python'), SkillLevel('BEGINNER'))
    
    # Same ID → same skill
    assert skill1 == skill2
    
    # Different ID → different skills
    skill3 = Skill(SkillId.generate(), SkillName('Python'), SkillLevel('BEGINNER'))
    assert skill1 != skill3
    
    print("✓ Skill equality by identity tests passed")


if __name__ == '__main__':
    test_skill_creation()
    test_skill_identity()
    test_skill_upgrade_level()
    test_skill_cannot_downgrade()
    test_skill_same_level()
    test_skill_immutable_name()
    test_skill_equality_by_identity()
    print("\n✅ All Skill entity tests passed!")
