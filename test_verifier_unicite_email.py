"""Tests for VerifierUniciteEmail Domain Service"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fake_demande_repository import FakeDemandeCompteFormateurRepository

from src.domain.formateur import (
    Email,
    CandidatInfo,
    Skill,
    SkillName,
    SkillLevel,
    DemandeCompteFormateur,
    VerifierUniciteEmail,
    EmailDejaUtiliseException,
)


def create_candidat_info(email: str = "test@example.com") -> CandidatInfo:
    """Helper: Create candidat info with custom email"""
    return CandidatInfo.create(
        first_name="Jean",
        last_name="Dupont",
        email=email
    )


def create_skills():
    """Helper: Create sample skills"""
    return [
        Skill.create(SkillName("Python"), SkillLevel.expert())
    ]


# ==================== TESTS ====================

def test_email_disponible():
    """Test that available email passes verification"""
    # Arrange
    repo = FakeDemandeCompteFormateurRepository()
    verifier = VerifierUniciteEmail(repo)
    email = Email("nouveau@example.com")

    # Act - should not raise
    verifier.execute(email)

    # Assert - if we get here, it passed
    print("✓ Email disponible test passed")


def test_email_deja_utilise():
    """Test that used email raises exception"""
    # Arrange
    repo = FakeDemandeCompteFormateurRepository()
    email = Email("existant@example.com")

    # Create existing demande
    demande = DemandeCompteFormateur.soumettre(
        create_candidat_info("existant@example.com"),
        create_skills()
    )
    repo.save(demande)

    # Act & Assert
    verifier = VerifierUniciteEmail(repo)

    try:
        verifier.execute(email)
        assert False, "Should have raised EmailDejaUtiliseException"
    except EmailDejaUtiliseException as e:
        assert e.email == email
        assert "déjà utilisé" in str(e).lower()

    print("✓ Email déjà utilisé test passed")


def test_est_disponible_true():
    """Test est_disponible returns True for available email"""
    # Arrange
    repo = FakeDemandeCompteFormateurRepository()
    verifier = VerifierUniciteEmail(repo)
    email = Email("nouveau@example.com")

    # Act
    disponible = verifier.est_disponible(email)

    # Assert
    assert disponible is True

    print("✓ Est disponible (True) test passed")


def test_est_disponible_false():
    """Test est_disponible returns False for used email"""
    # Arrange
    repo = FakeDemandeCompteFormateurRepository()
    email = Email("existant@example.com")

    demande = DemandeCompteFormateur.soumettre(
        create_candidat_info("existant@example.com"),
        create_skills()
    )
    repo.save(demande)

    verifier = VerifierUniciteEmail(repo)

    # Act
    disponible = verifier.est_disponible(email)

    # Assert
    assert disponible is False

    print("✓ Est disponible (False) test passed")


def test_emails_differents_disponibles():
    """Test that different emails don't conflict"""
    # Arrange
    repo = FakeDemandeCompteFormateurRepository()

    # Save demande with email1
    demande1 = DemandeCompteFormateur.soumettre(
        create_candidat_info("email1@example.com"),
        create_skills()
    )
    repo.save(demande1)

    verifier = VerifierUniciteEmail(repo)

    # Act - check different email
    email2 = Email("email2@example.com")
    verifier.execute(email2)  # Should not raise

    # Assert - if we get here, it passed
    print("✓ Emails différents disponibles test passed")


# ==================== RUN TESTS ====================

if __name__ == '__main__':
    test_email_disponible()
    test_email_deja_utilise()
    test_est_disponible_true()
    test_est_disponible_false()
    test_emails_differents_disponibles()

    print("\n✅ All VerifierUniciteEmail tests passed!")
