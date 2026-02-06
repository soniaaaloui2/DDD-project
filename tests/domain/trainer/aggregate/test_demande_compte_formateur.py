"""Tests for TrainerAccountRequest Aggregate"""

from datetime import datetime
import pytest

from src.domain.trainer import (
    # Value Objects
    RequestId,
    CandidatInfo,
    Email,
    FullName,
    RequestStatus,
    MotifRejet,
    FormateurId,
    SkillName,
    SkillLevel,
    # Entities
    Skill,
    # Aggregate
    TrainerAccountRequest,
    # Exceptions
    RequiredSkillsException,
    DemandeNonValidableException,
    DemandeNonRejetableException,
    # Events
    TrainerAccountRequestSubmitted,
    DemandeCompteFormateurValidee,
    DemandeCompteFormateurRejetee,
)


# ==================== HELPER FUNCTIONS ====================

def create_candidat_info() -> CandidatInfo:
    """Helper: Create a valid CandidatInfo"""
    return CandidatInfo.create(
        first_name="Jean",
        last_name="Dupont",
        email="jean.dupont@example.com"
    )


def create_skills() -> list[Skill]:
    """Helper: Create a list of valid skills"""
    return [
        Skill.create(SkillName("Python"), SkillLevel.expert()),
        Skill.create(SkillName("Java"), SkillLevel.intermediate()),
    ]


# ==================== TESTS: FACTORY METHOD ====================

def test_soumettre_demande():
    """Test submitting a new request"""
    candidat_info = create_candidat_info()
    skills = create_skills()

    # Act
    demande = DemandeCompteFormateur.soumettre(candidat_info, skills)

    # Assert
    assert demande.id is not None  # Has an ID
    assert demande.candidate_info == candidat_info
    assert len(demande.skills) == 2
    assert demande.statut == RequestStatus.pending_validation()
    assert demande.submission_date is not None
    assert demande.rejection_reason is None

    print("✓ Soumettre demande test passed")


def test_soumettre_sans_competences():
    """Test that submitting without skills raises exception"""
    candidat_info = create_candidat_info()

    # Act & Assert
    with pytest.raises(RequiredSkillsException):
        TrainerAccountRequest.submit(candidat_info, [])

    print("✓ Soumettre sans compétences test passed")


def test_soumettre_leve_evenement():
    """Test that submitting raises a domain event"""
    candidat_info = create_candidat_info()
    skills = create_skills()

    # Act
    demande = DemandeCompteFormateur.soumettre(candidat_info, skills)

    # Assert
    assert len(demande.events) == 1
    event = demande.events[0]
    assert isinstance(event, TrainerAccountRequestSubmitted)
    assert event.request_id == demande.id
    assert event.candidate_email == candidat_info.email

    print("✓ Soumettre lève événement test passed")


# ==================== TESTS: VALIDER ====================

def test_valider_demande():
    """Test approving a request"""
    # Arrange
    demande = TrainerAccountRequest.submit(create_candidat_info(), create_skills())
    admin_id = FormateurId.generate()
    demande.clear_events()  # Clear submission event

    # Act
    demande.approve(admin_id)

    # Assert
    assert demande.statut == RequestStatus.approved()

    # Event raised
    assert len(demande.events) == 1
    event = demande.events[0]
    assert isinstance(event, DemandeCompteFormateurValidee)
    assert event.request_Id == demande.id
    assert event.valide_par_admin_id == admin_id

    print("✓ Approve request test passed")


def test_valider_demande_deja_validee():
    """Test that approving an already approved request raises exception"""
    # Arrange
    demande = TrainerAccountRequest.submit(create_candidat_info(), create_skills())
    admin_id = FormateurId.generate()
    demande.approve(admin_id)

    # Act & Assert
    with pytest.raises(DemandeNonValidableException) as exc_info:
        demande.approve(admin_id)

    assert exc_info.value.request_Id == demande.id

    print("✓ Valider demande déjà validée test passed")


def test_valider_demande_rejetee():
    """Test that validating a rejected request raises exception"""
    # Arrange
    demande = TrainerAccountRequest.submit(create_candidat_info(), create_skills())
    admin_id = FormateurId.generate()
    demande.reject(admin_id, MotifRejet("Qualifications insuffisantes"))

    # Act & Assert
    with pytest.raises(DemandeNonValidableException):
        demande.approve(admin_id)

    print("✓ Approve rejected request test passed")


# ==================== TESTS: REJETER ====================

def test_rejeter_demande():
    """Test rejecting a request"""
    # Arrange
    demande = TrainerAccountRequest.submit(create_candidat_info(), create_skills())
    admin_id = FormateurId.generate()
    motif = MotifRejet("Expérience insuffisante dans le domaine")
    demande.clear_events()

    # Act
    demande.reject(admin_id, motif)

    # Assert
    assert demande.statut == RequestStatus.rejected()
    assert demande.rejection_reason == motif

    # Event raised
    assert len(demande.events) == 1
    event = demande.events[0]
    assert isinstance(event, DemandeCompteFormateurRejetee)
    assert event.request_Id == demande.id
    assert event.rejete_par_admin_id == admin_id
    assert event.motif == motif

    print("✓ Reject request test passed")


def test_rejeter_demande_deja_validee():
    """Test that rejecting an approved request raises exception"""
    # Arrange
    demande = TrainerAccountRequest.submit(create_candidat_info(), create_skills())
    admin_id = FormateurId.generate()
    demande.approve(admin_id)

    # Act & Assert
    with pytest.raises(DemandeNonRejetableException):
        demande.reject(admin_id, MotifRejet("Motif quelconque"))

    print("✓ Reject approved request test passed")


# ==================== TESTS: SKILLS ====================

def test_ajouter_skill():
    """Test adding a skill to a pending request"""
    # Arrange
    demande = TrainerAccountRequest.submit(create_candidat_info(), create_skills())
    initial_count = demande.count_skills()

    # Act
    new_skill = Skill.create(SkillName("JavaScript"), SkillLevel.beginner())
    demande.add_skill(new_skill)

    # Assert
    assert demande.count_skills() == initial_count + 1

    print("✓ Ajouter skill test passed")


def test_ajouter_skill_demande_validee():
    """Test that adding a skill to an approved request raises exception"""
    # Arrange
    demande = TrainerAccountRequest.submit(create_candidat_info(), create_skills())
    admin_id = FormateurId.generate()
    demande.approve(admin_id)

    # Act & Assert
    with pytest.raises(ValueError):
        demande.add_skill(Skill.create(SkillName("Ruby"), SkillLevel.beginner()))

    print("✓ Add skill to approved request test passed")


# ==================== TESTS: AGGREGATE RULES ====================

def test_aggregate_identity():
    """Test that aggregate has global identity"""
    demande1 = TrainerAccountRequest.submit(create_candidat_info(), create_skills())
    demande2 = TrainerAccountRequest.submit(create_candidat_info(), create_skills())

    # Different aggregates have different IDs
    assert demande1.id != demande2.id
    assert demande1 != demande2

    print("✓ Aggregate identity test passed")


def test_skills_encapsulation():
    """Test that skills list is protected (returned as copy)"""
    demande = TrainerAccountRequest.submit(create_candidat_info(), create_skills())

    # Get skills
    skills = demande.skills
    initial_count = len(skills)

    # Try to modify the returned list
    skills.append(Skill.create(SkillName("Ruby"), SkillLevel.beginner()))

    # Internal state should not be affected
    assert demande.count_skills() == initial_count

    print("✓ Skills encapsulation test passed")


def test_clear_events():
    """Test clearing domain events"""
    demande = TrainerAccountRequest.submit(create_candidat_info(), create_skills())

    assert len(demande.events) == 1

    demande.clear_events()

    assert len(demande.events) == 0

    print("✓ Clear events test passed")



if __name__ == '__main__':
    test_soumettre_demande()
    test_soumettre_sans_competences()
    test_soumettre_leve_evenement()
    test_valider_demande()
    test_valider_demande_deja_validee()
    test_valider_demande_rejetee()
    test_rejeter_demande()
    test_rejeter_demande_deja_validee()
    test_ajouter_skill()
    test_ajouter_skill_demande_validee()
    test_aggregate_identity()
    test_skills_encapsulation()
    test_clear_events()

    print("\nAll TrainerAccountRequest tests passed!")
