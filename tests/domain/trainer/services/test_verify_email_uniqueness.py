"""Tests pour le service de vérification d'unicité d'email"""

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
    VerifyEmailUniqueness,
    EmailAlreadyUsedException,
)

from tests.domain.trainer.repositories.in_memory_trainer_account_request_repository import (
    InMemoryTrainerAccountRequestRepository
)


def create_candidat_info(email: str = "test@example.com") -> CandidatInfo:
    return CandidatInfo.create(
        first_name="Jean",
        last_name="Dupont",
        email=email
    )


def create_skills():
    return [Skill.create(SkillName("Python"), SkillLevel.expert())]


def test_email_available():
    repo = InMemoryTrainerAccountRequestRepository()
    verifier = VerifyEmailUniqueness(repo)
    email = Email("nouveau@example.com")

    verifier.execute(email)

    print("Email available test passed")


def test_email_already_used():
    repo = InMemoryTrainerAccountRequestRepository()
    email = Email("existant@example.com")

    request = TrainerAccountRequest.submit(
        create_candidat_info("existant@example.com"),
        create_skills()
    )
    repo.save(request)

    verifier = VerifyEmailUniqueness(repo)

    try:
        verifier.execute(email)
        assert False, "Should have raised EmailAlreadyUsedException"
    except EmailAlreadyUsedException as e:
        assert e.email == email
        assert "already" in str(e).lower()

    print("Email already used test passed")


def test_is_available_true():
    repo = InMemoryTrainerAccountRequestRepository()
    verifier = VerifyEmailUniqueness(repo)
    email = Email("nouveau@example.com")

    available = verifier.is_available(email)

    assert available is True

    print("Is available (True) test passed")


def test_is_available_false():
    repo = InMemoryTrainerAccountRequestRepository()
    email = Email("existant@example.com")

    request = TrainerAccountRequest.submit(
        create_candidat_info("existant@example.com"),
        create_skills()
    )
    repo.save(request)

    verifier = VerifyEmailUniqueness(repo)

    available = verifier.is_available(email)

    assert available is False

    print("Is available (False) test passed")


def test_different_emails_dont_conflict():
    repo = InMemoryTrainerAccountRequestRepository()

    request1 = TrainerAccountRequest.submit(
        create_candidat_info("email1@example.com"),
        create_skills()
    )
    repo.save(request1)

    verifier = VerifyEmailUniqueness(repo)

    email2 = Email("email2@example.com")
    verifier.execute(email2)

    print("Different emails don't conflict test passed")


def test_case_insensitive_email_check():
    repo = InMemoryTrainerAccountRequestRepository()

    request = TrainerAccountRequest.submit(
        create_candidat_info("user@example.com"),
        create_skills()
    )
    repo.save(request)

    verifier = VerifyEmailUniqueness(repo)

    try:
        verifier.execute(Email("USER@EXAMPLE.COM"))
        assert False, "Should have raised EmailAlreadyUsedException"
    except EmailAlreadyUsedException:
        pass

    print("Case-insensitive email check test passed")


if __name__ == '__main__':
    test_email_available()
    test_email_already_used()
    test_is_available_true()
    test_is_available_false()
    test_different_emails_dont_conflict()
    test_case_insensitive_email_check()

    print("\nAll VerifyEmailUniqueness tests passed!")
