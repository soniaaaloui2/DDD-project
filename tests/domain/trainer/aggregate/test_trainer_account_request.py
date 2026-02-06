"""Tests for TrainerAccountRequest Aggregate (USE CASE 1 ONLY)"""

import sys
from pathlib import Path
import pytest

# Add src directory to path
src_path = Path(__file__).parent.parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

from domain.trainer import (
    # Value Objects
    RequestId,
    CandidatInfo,
    RequestStatus,
    SkillName,
    SkillLevel,
    # Entities
    Skill,
    # Aggregate
    TrainerAccountRequest,
    # Exceptions
    RequiredSkillsException,
    # Events
    TrainerAccountRequestSubmitted,
)


# ==================== HELPER FUNCTIONS ====================

def create_candidat_info(email: str = "jean.dupont@example.com") -> CandidatInfo:
    """Helper: Create a valid CandidatInfo"""
    return CandidatInfo.create(
        first_name="Jean",
        last_name="Dupont",
        email=email
    )


def create_skills() -> list[Skill]:
    """Helper: Create a list of valid skills"""
    return [
        Skill.create(SkillName("Python"), SkillLevel.expert()),
        Skill.create(SkillName("Java"), SkillLevel.intermediate()),
    ]


# ==================== TESTS: SUBMIT (USE CASE 1) ====================

def test_submit_request():
    """Test submitting a new request"""
    # Arrange
    candidat_info = create_candidat_info()
    skills = create_skills()

    # Act
    request = TrainerAccountRequest.submit(candidat_info, skills)

    # Assert
    assert request.id is not None
    assert request.candidate_info == candidat_info
    assert len(request.skills) == 2
    assert request.statut == RequestStatus.pending_validation()
    assert request.submission_date is not None

    print("✓ Submit request test passed")


def test_submit_without_skills():
    """Test that submitting without skills raises exception"""
    # Arrange
    candidat_info = create_candidat_info()

    # Act & Assert
    with pytest.raises(RequiredSkillsException):
        TrainerAccountRequest.submit(candidat_info, [])

    print("✓ Submit without skills test passed")


def test_submit_raises_event():
    """Test that submitting raises a domain event"""
    # Arrange
    candidat_info = create_candidat_info()
    skills = create_skills()

    # Act
    request = TrainerAccountRequest.submit(candidat_info, skills)

    # Assert - Event raised
    assert len(request.events) == 1
    event = request.events[0]
    assert isinstance(event, TrainerAccountRequestSubmitted)
    assert event.request_id == request.id
    assert event.candidate_email == candidat_info.email

    print("✓ Submit raises event test passed")


# ==================== TESTS: AGGREGATE RULES ====================

def test_aggregate_identity():
    """Test that aggregate has global identity"""
    # Arrange & Act
    request1 = TrainerAccountRequest.submit(
        create_candidat_info("user1@example.com"),
        create_skills()
    )
    request2 = TrainerAccountRequest.submit(
        create_candidat_info("user2@example.com"),
        create_skills()
    )

    # Assert - Different aggregates have different IDs
    assert request1.id != request2.id
    assert request1 != request2

    print("✓ Aggregate identity test passed")


def test_skills_encapsulation():
    """Test that skills list is protected (returned as copy)"""
    # Arrange
    request = TrainerAccountRequest.submit(create_candidat_info(), create_skills())

    # Act - Get skills and try to modify
    skills = request.skills
    initial_count = len(skills)
    skills.append(Skill.create(SkillName("Ruby"), SkillLevel.beginner()))

    # Assert - Internal state should not be affected
    assert len(request.skills) == initial_count

    print("✓ Skills encapsulation test passed")


def test_clear_events():
    """Test clearing domain events"""
    # Arrange
    request = TrainerAccountRequest.submit(create_candidat_info(), create_skills())
    assert len(request.events) == 1

    # Act
    request.clear_events()

    # Assert
    assert len(request.events) == 0

    print("✓ Clear events test passed")


def test_constructor_validates_skills():
    """Test that constructor validates skills requirement"""
    # Arrange
    candidat_info = create_candidat_info()

    # Act & Assert - Direct constructor call should also validate
    with pytest.raises(RequiredSkillsException):
        TrainerAccountRequest(
            request_id=RequestId.generate(),
            candidate_info=candidat_info,
            skills=[],  # Empty skills
            status=RequestStatus.pending_validation(),
            submission_date=datetime.now(),
        )

    print("✓ Constructor validates skills test passed")


# ==================== RUN TESTS ====================

if __name__ == '__main__':
    from datetime import datetime

    test_submit_request()
    test_submit_without_skills()
    test_submit_raises_event()
    test_aggregate_identity()
    test_skills_encapsulation()
    test_clear_events()
    test_constructor_validates_skills()

    print("\n✅ All TrainerAccountRequest tests passed!")
