"""Tests pour la demande de compte formateur"""

import sys
from pathlib import Path
from datetime import datetime
import pytest

src_path = Path(__file__).parent.parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from domain.trainer import (
    RequestId,
    CandidatInfo,
    RequestStatus,
    SkillName,
    SkillLevel,
    Skill,
    TrainerAccountRequest,
    RequiredSkillsException,
    TrainerAccountRequestSubmitted,
)

def create_candidat_info(email: str = "jean.dupont@example.com") -> CandidatInfo:
    return CandidatInfo.create(
        first_name="Jean",
        last_name="Dupont",
        email=email
    )


def create_skills() -> list[Skill]:
    return [
        Skill.create(SkillName("Python"), SkillLevel.expert()),
        Skill.create(SkillName("Java"), SkillLevel.intermediate()),
    ]



def test_submit_request():
    candidat_info = create_candidat_info()
    skills = create_skills()

    request = TrainerAccountRequest.submit(candidat_info, skills)

    assert request.id is not None
    assert request.candidate_info == candidat_info
    assert len(request.skills) == 2
    assert request.statut == RequestStatus.pending_validation()
    assert request.submission_date is not None

    print("Submit request test passed")


def test_submit_without_skills():
    candidat_info = create_candidat_info()

    with pytest.raises(RequiredSkillsException):
        TrainerAccountRequest.submit(candidat_info, [])

    print("Submit without skills test passed")


def test_submit_raises_event():
    candidat_info = create_candidat_info()
    skills = create_skills()

    request = TrainerAccountRequest.submit(candidat_info, skills)

    assert len(request.events) == 1
    event = request.events[0]
    assert isinstance(event, TrainerAccountRequestSubmitted)
    assert event.request_id == request.id
    assert event.candidate_email == candidat_info.email

    print("Submit raises event test passed")


def test_aggregate_has_global_identity():
    request1 = TrainerAccountRequest.submit(
        create_candidat_info("user1@example.com"),
        create_skills()
    )
    request2 = TrainerAccountRequest.submit(
        create_candidat_info("user2@example.com"),
        create_skills()
    )

    assert request1.id != request2.id
    assert request1 != request2

    print("Aggregate identity test passed")


def test_skills_encapsulation():
    request = TrainerAccountRequest.submit(create_candidat_info(), create_skills())

    skills = request.skills
    initial_count = len(skills)
    skills.append(Skill.create(SkillName("Ruby"), SkillLevel.beginner()))

    assert len(request.skills) == initial_count

    print("Skills encapsulation test passed")


def test_clear_events():
    request = TrainerAccountRequest.submit(create_candidat_info(), create_skills())
    assert len(request.events) == 1

    request.clear_events()

    assert len(request.events) == 0

    print("Clear events test passed")


def test_constructor_validates_skills():
    candidat_info = create_candidat_info()

    with pytest.raises(RequiredSkillsException):
        TrainerAccountRequest(
            request_id=RequestId.generate(),
            candidate_info=candidat_info,
            skills=[],
            status=RequestStatus.pending_validation(),
            submission_date=datetime.now(),
        )

    print("Constructor validates skills test passed")


if __name__ == '__main__':
    from datetime import datetime

    test_submit_request()
    test_submit_without_skills()
    test_submit_raises_event()
    test_aggregate_has_global_identity()
    test_skills_encapsulation()
    test_clear_events()
    test_constructor_validates_skills()

    print("\nAll TrainerAccountRequest Aggregate tests passed!")
