"""Tests for Value Objects"""

from src.domain.formateur import (
    Email, FormateurId, FullName, SkillLevel, OnboardingStatus, SkillId, SkillName
)


def test_email():
    email = Email('john@example.com')
    assert email.value == 'john@example.com'
    
    email2 = Email('JOHN@EXAMPLE.COM')
    assert email2.value == 'john@example.com'
    
    email3 = Email('john@example.com')
    assert email == email3
    
    try:
        Email('invalid-email')
        assert False
    except ValueError:
        pass
    
    print("ok Email tests passed")


def test_formateur_id():
    id1 = FormateurId.generate()
    id2 = FormateurId.generate()
    assert id1 != id2
    
    id_str = str(id1)
    id3 = FormateurId.from_string(id_str)
    assert id1 == id3
    
    print("ok FormateurId tests passed")


def test_full_name():
    name = FullName('john', 'doe')
    assert name.first_name == 'John'
    assert name.last_name == 'Doe'
    assert name.full_name() == 'John Doe'
    
    name2 = FullName('john', 'doe')
    assert name == name2
    
    print("ok FullName tests passed")


def test_skill_id():
    skill_id = SkillId.generate()
    assert skill_id.value
    
    print("ok SkillId tests passed")


def test_skill_name():
    skill_name = SkillName('Python')
    assert skill_name.value == 'Python'
    
    skill_name2 = SkillName('python')
    assert skill_name == skill_name2
    
    print("ok SkillName tests passed")


def test_skill_level():
    beginner = SkillLevel('BEGINNER')
    intermediate = SkillLevel('INTERMEDIATE')
    expert = SkillLevel('EXPERT')
    
    assert expert.is_at_least(beginner)
    assert not beginner.is_at_least(expert)
    
    assert SkillLevel.expert().value == 'EXPERT'
    
    print("ok SkillLevel tests passed")


def test_onboarding_status():
    started = OnboardingStatus.initial()
    skills_completed = OnboardingStatus('SKILLS_COMPLETED')
    
    assert started.can_transition_to(skills_completed)
    assert not skills_completed.can_transition_to(started)
    
    assert skills_completed.is_at_least('STARTED')
    assert not started.is_at_least('SKILLS_COMPLETED')
    
    print("ok OnboardingStatus tests passed")


if __name__ == '__main__':
    test_email()
    test_formateur_id()
    test_full_name()
    test_skill_id()
    test_skill_name()
    test_skill_level()
    test_onboarding_status()
    print("\nok All tests passed!")
