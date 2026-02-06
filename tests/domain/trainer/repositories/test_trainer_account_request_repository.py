"""Tests pour le repository de demande de compte formateur"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent.parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(project_root))

from domain.trainer import (
    Email,
    CandidatInfo,
    Skill,
    SkillName,
    SkillLevel,
    TrainerAccountRequest,
    RequestStatus,
)

from tests.domain.trainer.repositories.in_memory_trainer_account_request_repository import (
    InMemoryTrainerAccountRequestRepository
)


def create_candidat_info(email: str = "test@example.com") -> CandidatInfo:
    return CandidatInfo.create("Jean", "Dupont", email)


def create_skills():
    return [Skill.create(SkillName("Python"), SkillLevel.expert())]


def test_save_and_find():
    repo = InMemoryTrainerAccountRequestRepository()
    request = TrainerAccountRequest.submit(
        create_candidat_info(),
        create_skills()
    )

    repo.save(request)
    found = repo.find(request.id)

    assert found is not None
    assert found.id == request.id
    assert found.candidate_info.email == request.candidate_info.email

    print("Save and find test passed")


def test_find_by_email():
    repo = InMemoryTrainerAccountRequestRepository()
    email = Email("specific@example.com")
    request = TrainerAccountRequest.submit(
        create_candidat_info("specific@example.com"),
        create_skills()
    )
    repo.save(request)

    found = repo.find_by_email(email)

    assert found is not None
    assert found.candidate_info.email == email

    print("Find by email test passed")


def test_find_pending_validation():
    repo = InMemoryTrainerAccountRequestRepository()

    request1 = TrainerAccountRequest.submit(
        create_candidat_info("pending1@example.com"),
        create_skills()
    )
    request2 = TrainerAccountRequest.submit(
        create_candidat_info("pending2@example.com"),
        create_skills()
    )
    repo.save(request1)
    repo.save(request2)

    pending = repo.find_pending_validation()

    assert len(pending) == 2

    print("Find pending validation test passed")


def test_exists_by_email():
    repo = InMemoryTrainerAccountRequestRepository()
    email = Email("exists@example.com")
    request = TrainerAccountRequest.submit(
        create_candidat_info("exists@example.com"),
        create_skills()
    )
    repo.save(request)

    assert repo.exists_by_email(email) is True
    assert repo.exists_by_email(Email("notexists@example.com")) is False

    print("Exists by email test passed")


def test_delete():
    repo = InMemoryTrainerAccountRequestRepository()
    request = TrainerAccountRequest.submit(
        create_candidat_info(),
        create_skills()
    )
    repo.save(request)

    repo.delete(request)

    assert repo.find(request.id) is None
    assert repo.count_all() == 0

    print("Delete test passed")


def test_clear():
    repo = InMemoryTrainerAccountRequestRepository()

    for i in range(5):
        request = TrainerAccountRequest.submit(
            create_candidat_info(f"user{i}@example.com"),
            create_skills()
        )
        repo.save(request)

    assert repo.count_all() == 5

    repo.clear()

    assert repo.count_all() == 0

    print("Clear test passed")


def test_find_by_status():
    repo = InMemoryTrainerAccountRequestRepository()

    for i in range(2):
        request = TrainerAccountRequest.submit(
            create_candidat_info(f"pending{i}@example.com"),
            create_skills()
        )
        repo.save(request)

    pending = repo.find_by_status(RequestStatus.pending_validation())

    assert len(pending) == 2

    print("Find by status test passed")


if __name__ == '__main__':
    test_save_and_find()
    test_find_by_email()
    test_find_pending_validation()
    test_exists_by_email()
    test_delete()
    test_clear()
    test_find_by_status()

    print("\nAll Repository tests passed!")
