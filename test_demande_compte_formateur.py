"""Tests for DemandeCompteFormateur Aggregate"""

from datetime import datetime
import pytest

from src.domain.formateur import (
    # Value Objects
    DemandeId,
    CandidatInfo,
    Email,
    FullName,
    StatutDemande,
    MotifRejet,
    FormateurId,
    SkillName,
    SkillLevel,
    # Entities
    Skill,
    # Aggregate
    DemandeCompteFormateur,
    # Exceptions
    CompetencesRequisesException,
    DemandeNonValidableException,
    DemandeNonRejetableException,
    # Events
    DemandeCompteFormateurSoumise,
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
    assert demande.candidat_info == candidat_info
    assert len(demande.skills) == 2
    assert demande.statut == StatutDemande.en_attente_validation()
    assert demande.date_soumission is not None
    assert demande.motif_rejet is None

    print("✓ Soumettre demande test passed")


def test_soumettre_sans_competences():
    """Test that submitting without skills raises exception"""
    candidat_info = create_candidat_info()

    # Act & Assert
    with pytest.raises(CompetencesRequisesException):
        DemandeCompteFormateur.soumettre(candidat_info, [])

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
    assert isinstance(event, DemandeCompteFormateurSoumise)
    assert event.demande_id == demande.id
    assert event.candidat_email == candidat_info.email

    print("✓ Soumettre lève événement test passed")


# ==================== TESTS: VALIDER ====================

def test_valider_demande():
    """Test validating a request"""
    # Arrange
    demande = DemandeCompteFormateur.soumettre(create_candidat_info(), create_skills())
    admin_id = FormateurId.generate()
    demande.clear_events()  # Clear submission event

    # Act
    demande.valider(admin_id)

    # Assert
    assert demande.statut == StatutDemande.validee()

    # Event raised
    assert len(demande.events) == 1
    event = demande.events[0]
    assert isinstance(event, DemandeCompteFormateurValidee)
    assert event.demande_id == demande.id
    assert event.valide_par_admin_id == admin_id

    print("✓ Valider demande test passed")


def test_valider_demande_deja_validee():
    """Test that validating an already validated request raises exception"""
    # Arrange
    demande = DemandeCompteFormateur.soumettre(create_candidat_info(), create_skills())
    admin_id = FormateurId.generate()
    demande.valider(admin_id)

    # Act & Assert
    with pytest.raises(DemandeNonValidableException) as exc_info:
        demande.valider(admin_id)

    assert exc_info.value.demande_id == demande.id

    print("✓ Valider demande déjà validée test passed")


def test_valider_demande_rejetee():
    """Test that validating a rejected request raises exception"""
    # Arrange
    demande = DemandeCompteFormateur.soumettre(create_candidat_info(), create_skills())
    admin_id = FormateurId.generate()
    demande.rejeter(admin_id, MotifRejet("Qualifications insuffisantes"))

    # Act & Assert
    with pytest.raises(DemandeNonValidableException):
        demande.valider(admin_id)

    print("✓ Valider demande rejetée test passed")


# ==================== TESTS: REJETER ====================

def test_rejeter_demande():
    """Test rejecting a request"""
    # Arrange
    demande = DemandeCompteFormateur.soumettre(create_candidat_info(), create_skills())
    admin_id = FormateurId.generate()
    motif = MotifRejet("Expérience insuffisante dans le domaine")
    demande.clear_events()

    # Act
    demande.rejeter(admin_id, motif)

    # Assert
    assert demande.statut == StatutDemande.rejetee()
    assert demande.motif_rejet == motif

    # Event raised
    assert len(demande.events) == 1
    event = demande.events[0]
    assert isinstance(event, DemandeCompteFormateurRejetee)
    assert event.demande_id == demande.id
    assert event.rejete_par_admin_id == admin_id
    assert event.motif == motif

    print("✓ Rejeter demande test passed")


def test_rejeter_demande_deja_validee():
    """Test that rejecting a validated request raises exception"""
    # Arrange
    demande = DemandeCompteFormateur.soumettre(create_candidat_info(), create_skills())
    admin_id = FormateurId.generate()
    demande.valider(admin_id)

    # Act & Assert
    with pytest.raises(DemandeNonRejetableException):
        demande.rejeter(admin_id, MotifRejet("Motif quelconque"))

    print("✓ Rejeter demande déjà validée test passed")


# ==================== TESTS: SKILLS ====================

def test_ajouter_skill():
    """Test adding a skill to a pending request"""
    # Arrange
    demande = DemandeCompteFormateur.soumettre(create_candidat_info(), create_skills())
    initial_count = demande.nombre_skills()

    # Act
    new_skill = Skill.create(SkillName("JavaScript"), SkillLevel.beginner())
    demande.ajouter_skill(new_skill)

    # Assert
    assert demande.nombre_skills() == initial_count + 1

    print("✓ Ajouter skill test passed")


def test_ajouter_skill_demande_validee():
    """Test that adding a skill to a validated request raises exception"""
    # Arrange
    demande = DemandeCompteFormateur.soumettre(create_candidat_info(), create_skills())
    admin_id = FormateurId.generate()
    demande.valider(admin_id)

    # Act & Assert
    with pytest.raises(ValueError):
        demande.ajouter_skill(Skill.create(SkillName("Ruby"), SkillLevel.beginner()))

    print("✓ Ajouter skill demande validée test passed")


# ==================== TESTS: AGGREGATE RULES ====================

def test_aggregate_identity():
    """Test that aggregate has global identity"""
    demande1 = DemandeCompteFormateur.soumettre(create_candidat_info(), create_skills())
    demande2 = DemandeCompteFormateur.soumettre(create_candidat_info(), create_skills())

    # Different aggregates have different IDs
    assert demande1.id != demande2.id
    assert demande1 != demande2

    print("✓ Aggregate identity test passed")


def test_skills_encapsulation():
    """Test that skills list is protected (returned as copy)"""
    demande = DemandeCompteFormateur.soumettre(create_candidat_info(), create_skills())

    # Get skills
    skills = demande.skills
    initial_count = len(skills)

    # Try to modify the returned list
    skills.append(Skill.create(SkillName("Ruby"), SkillLevel.beginner()))

    # Internal state should not be affected
    assert demande.nombre_skills() == initial_count

    print("✓ Skills encapsulation test passed")


def test_clear_events():
    """Test clearing domain events"""
    demande = DemandeCompteFormateur.soumettre(create_candidat_info(), create_skills())

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

    print("\nAll DemandeCompteFormateur tests passed!")
