"""Tests pour les value objects du domaine Formateur"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from domain.trainer import (
    Email, FullName, SkillLevel, SkillId, SkillName, RequestId, RequestStatus, CandidatInfo
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

    print("Email tests passed")

def test_full_name():
    name = FullName('john', 'doe')
    assert name.first_name == 'John'
    assert name.last_name == 'Doe'
    assert name.full_name() == 'John Doe'

    name2 = FullName('john', 'doe')
    assert name == name2

    print("FullName tests passed")


def test_skill_id():
    skill_id = SkillId.generate()
    assert skill_id.value

    print("SkillId tests passed")


def test_skill_name():
    skill_name = SkillName('Python')
    assert skill_name.value == 'Python'

    skill_name2 = SkillName('python')
    assert skill_name == skill_name2

    print("SkillName tests passed")


def test_skill_level():
    beginner = SkillLevel('BEGINNER')
    intermediate = SkillLevel('INTERMEDIATE')
    expert = SkillLevel('EXPERT')

    assert expert.is_at_least(beginner)
    assert not beginner.is_at_least(expert)

    assert SkillLevel.expert().value == 'EXPERT'

    print("SkillLevel tests passed")


def test_request_id():
    id1 = RequestId.generate()
    id2 = RequestId.generate()
    assert id1 != id2

    id_str = str(id1)
    id3 = RequestId.from_string(id_str)
    assert id1 == id3

    print("RequestId tests passed")


def test_request_status():
    pending = RequestStatus.pending_validation()
    approved = RequestStatus.approved()
    rejected = RequestStatus.rejected()

    assert pending.can_be_approved()
    assert pending.can_be_rejected()
    assert not approved.can_be_approved()

    assert approved.is_final()
    assert rejected.is_final()
    assert not pending.is_final()

    print("RequestStatus tests passed")


def test_candidat_info():
    email = Email('john@example.com')
    full_name = FullName('john', 'doe')

    candidat_info = CandidatInfo(full_name, email)
    assert candidat_info.full_name == full_name
    assert candidat_info.email == email
    assert candidat_info.is_complete()

    candidat_info2 = CandidatInfo.create('john', 'doe', 'john@example.com')
    assert candidat_info2.full_name.first_name == 'John'
    assert candidat_info2.email.value == 'john@example.com'
    assert candidat_info2.is_complete()

    assert candidat_info == candidat_info2

    str_repr = str(candidat_info)
    assert 'John Doe' in str_repr
    assert 'john@example.com' in str_repr

    print("CandidatInfo tests passed")


if __name__ == '__main__':
    test_email()
    test_full_name()
    test_skill_id()
    test_skill_name()
    test_skill_level()
    test_request_id()
    test_request_status()
    test_candidat_info()
    print("\nAll tests passed!")
