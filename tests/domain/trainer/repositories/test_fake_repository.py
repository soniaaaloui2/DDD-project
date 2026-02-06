"""Tests for FakeDemandeCompteFormateurRepository"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fake_demande_repository import FakeDemandeCompteFormateurRepository

from src.domain.trainer import (
    Email,
    CandidatInfo,
    Skill,
    SkillName,
    SkillLevel,
    DemandeCompteFormateur,
    RequestStatus,
    FormateurId,
    MotifRejet,
)


def create_candidat_info(email: str = "test@example.com") -> CandidatInfo:
    """Helper"""
    return CandidatInfo.create("Jean", "Dupont", email)


def create_skills():
    """Helper"""
    return [Skill.create(SkillName("Python"), SkillLevel.expert())]


# ==================== TESTS ====================

def test_save_and_find():
    """Test saving and finding by ID"""
    # Arrange
    repo = FakeDemandeCompteFormateurRepository()
    demande = DemandeCompteFormateur.soumettre(
        create_candidat_info(),
        create_skills()
    )

    # Act
    repo.save(demande)
    found = repo.find(demande.id)

    # Assert
    assert found is not None
    assert found.id == demande.id
    assert found.candidat_info.email == demande.candidat_info.email

    print("✓ Save and find test passed")


def test_find_by_email():
    """Test finding by email"""
    # Arrange
    repo = FakeDemandeCompteFormateurRepository()
    email = Email("specific@example.com")
    demande = DemandeCompteFormateur.soumettre(
        create_candidat_info("specific@example.com"),
        create_skills()
    )
    repo.save(demande)

    # Act
    found = repo.find_by_email(email)

    # Assert
    assert found is not None
    assert found.candidat_info.email == email

    print("✓ Find by email test passed")


def test_find_pending_validation():
    """Test finding pending requests"""
    # Arrange
    repo = FakeDemandeCompteFormateurRepository()

    # Create pending demande
    demande1 = DemandeCompteFormateur.soumettre(
        create_candidat_info("pending@example.com"),
        create_skills()
    )
    repo.save(demande1)

    # Create validated demande
    demande2 = DemandeCompteFormateur.soumettre(
        create_candidat_info("validated@example.com"),
        create_skills()
    )
    demande2.valider(FormateurId.generate())
    repo.save(demande2)

    # Act
    pending = repo.find_pending_validation()

    # Assert
    assert len(pending) == 1
    assert pending[0].id == demande1.id

    print("✓ Find en attente validation test passed")


def test_exists_by_email():
    """Test email existence check"""
    # Arrange
    repo = FakeDemandeCompteFormateurRepository()
    email = Email("exists@example.com")
    demande = DemandeCompteFormateur.soumettre(
        create_candidat_info("exists@example.com"),
        create_skills()
    )
    repo.save(demande)

    # Act & Assert
    assert repo.exists_by_email(email) is True
    assert repo.exists_by_email(Email("notexists@example.com")) is False

    print("✓ Exists by email test passed")


def test_count_by_statut():
    """Test counting by status"""
    # Arrange
    repo = FakeDemandeCompteFormateurRepository()

    # Create 2 pending
    for i in range(2):
        demande = DemandeCompteFormateur.soumettre(
            create_candidat_info(f"pending{i}@example.com"),
            create_skills()
        )
        repo.save(demande)

    # Create 1 validated
    demande_validated = DemandeCompteFormateur.soumettre(
        create_candidat_info("validated@example.com"),
        create_skills()
    )
    demande_validated.valider(FormateurId.generate())
    repo.save(demande_validated)

    # Act & Assert
    assert repo.count_by_statut(RequestStatus.pending_validation()) == 2
    assert repo.count_by_statut(RequestStatus.approved()) == 1
    assert repo.count_by_statut(RequestStatus.rejected()) == 0

    print("✓ Count by statut test passed")


def test_delete():
    """Test deleting a demande"""
    # Arrange
    repo = FakeDemandeCompteFormateurRepository()
    demande = DemandeCompteFormateur.soumettre(
        create_candidat_info(),
        create_skills()
    )
    repo.save(demande)

    # Act
    repo.delete(demande)

    # Assert
    assert repo.find(demande.id) is None
    assert repo.count_all() == 0

    print("✓ Delete test passed")


# ==================== RUN TESTS ====================

if __name__ == '__main__':
    test_save_and_find()
    test_find_by_email()
    test_find_pending_validation()
    test_exists_by_email()
    test_count_by_statut()
    test_delete()

    print("\n✅ All FakeRepository tests passed!")
