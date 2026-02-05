"""DemandeCompteFormateur - Aggregate Root for trainer account requests"""

from datetime import datetime
from typing import List, Optional

from src.domain.shared import Entity
from src.domain.formateur.value_objects import (
    DemandeId,
    CandidatInfo,
    StatutDemande,
    FormateurId,
    MotifRejet,
)
from src.domain.formateur.entities import Skill
from src.domain.formateur.events import (
    DemandeCompteFormateurSoumise,
    DemandeCompteFormateurValidee,
    DemandeCompteFormateurRejetee,
)
from src.domain.formateur.exceptions import (
    CompetencesRequisesException,
    DemandeNonValidableException,
    DemandeNonRejetableException,
)


class DemandeCompteFormateur(Entity[DemandeId]):
    """
    DemandeCompteFormateur - Aggregate Root

    Represents a trainer account request submitted by a candidate.

    AGGREGATE RULES (from course - 7 rules of Eric Evans):

    1. Global Identity of Root ✓
       - Has DemandeId (globally accessible)

    2. Local Identity for Internal Entities ✓
       - Skills have SkillId (only meaningful within this Demande)

    3. No Direct Reference to Internal Entities ✓
       - External code cannot access Skills directly
       - Must go through DemandeCompteFormateur

    4. Access Only Through Root ✓
       - Repository loads/saves the entire Aggregate

    5. Outgoing References by ID ✓
       - References FormateurId (admin), not the full Formateur object

    6. Cascade Delete ✓
       - Deleting Demande deletes all its Skills

    7. Invariants Satisfied ✓
       - All business rules enforced

    INVARIANTS (Business Rules):
    - A request must have at least one skill
    - Status transitions are controlled
    - Once validated, cannot be rejected
    - Once rejected, cannot be validated
    - Rejection requires a reason

    LIFECYCLE:
    1. Created (via soumettre factory)
    2. EN_ATTENTE_VALIDATION
    3. → VALIDEE or REJETEE (final states)
    """

    def __init__(
        self,
        demande_id: DemandeId,
        candidat_info: CandidatInfo,
        skills: List[Skill],
        statut: StatutDemande,
        date_soumission: datetime,
        motif_rejet: Optional[MotifRejet] = None,
    ):
        """
        Private constructor - use factory methods instead.

        Args:
            demande_id: Unique identifier
            candidat_info: Candidate information
            skills: List of candidate skills
            statut: Current status
            date_soumission: Submission date
            motif_rejet: Rejection reason (if rejected)
        """
        super().__init__(demande_id)

        # Validate invariants
        if not skills:
            raise CompetencesRequisesException()

        self._candidat_info = candidat_info
        self._skills = list(skills)  # Copy to protect internal state
        self._statut = statut
        self._date_soumission = date_soumission
        self._motif_rejet = motif_rejet

        # Domain Events collection
        self._events: List = []

    @property
    def candidat_info(self) -> CandidatInfo:
        """Get candidate information (immutable)"""
        return self._candidat_info

    @property
    def skills(self) -> List[Skill]:
        """Get skills (returns copy to protect internal state)"""
        return list(self._skills)

    @property
    def statut(self) -> StatutDemande:
        """Get current status"""
        return self._statut

    @property
    def date_soumission(self) -> datetime:
        """Get submission date"""
        return self._date_soumission

    @property
    def motif_rejet(self) -> Optional[MotifRejet]:
        """Get rejection reason (if rejected)"""
        return self._motif_rejet

    @property
    def events(self) -> List:
        """Get domain events (for infrastructure to publish)"""
        return list(self._events)


    @staticmethod
    def soumettre(
        candidat_info: CandidatInfo,
        skills: List[Skill]
    ) -> 'DemandeCompteFormateur':
        """
        FACTORY METHOD - Submit a new trainer account request

        This is the ONLY way to create a new DemandeCompteFormateur.

        Business flow (from use case):
        1. Candidate fills form
        2. Candidate submits
        3. System creates request with status EN_ATTENTE_VALIDATION
        4. System publishes DemandeCompteFormateurSoumise event

        Args:
            candidat_info: Validated candidate information
            skills: List of candidate skills (at least 1)

        Returns:
            New DemandeCompteFormateur with initial state

        Raises:
            CompetencesRequisesException: If skills list is empty

        What this guarantees (from course):
        ✓ Expressive name: soumettre() (business vocabulary)
        ✓ Invariants guaranteed: status is EN_ATTENTE_VALIDATION
        ✓ ID auto-generated: caller doesn't manage IDs
        ✓ Initial state forced: cannot create in wrong state
        ✓ Event automatically raised: cannot forget
        """
        # Validate business rule
        if not skills:
            raise CompetencesRequisesException()

        # Create the aggregate
        demande = DemandeCompteFormateur(
            demande_id=DemandeId.generate(),  # ← ID auto-generated
            candidat_info=candidat_info,
            skills=skills,
            statut=StatutDemande.en_attente_validation(),  # ← Initial state forced
            date_soumission=datetime.now(),
            motif_rejet=None,
        )

        # Raise domain event
        demande._record_event(
            DemandeCompteFormateurSoumise(
                demande_id=demande.id,
                candidat_email=candidat_info.email,
            )
        )

        return demande

    # ==================== BUSINESS METHODS ====================

    def valider(self, admin_id: FormateurId) -> None:
        """
        Validate the request (admin action)

        Business flow:
        1. Admin reviews request
        2. Admin approves
        3. Status changes to VALIDEE
        4. Event raised for listeners to create account

        Args:
            admin_id: ID of the admin who validated

        Raises:
            DemandeNonValidableException: If not in EN_ATTENTE_VALIDATION
        """
        # Check business rule: can only validate if EN_ATTENTE
        if not self._statut.peut_etre_validee():
            raise DemandeNonValidableException(self.id, self._statut)

        # Change state
        self._statut = StatutDemande.validee()

        # Raise domain event
        self._record_event(
            DemandeCompteFormateurValidee(
                demande_id=self.id,
                valide_par_admin_id=admin_id,
            )
        )

    def rejeter(self, admin_id: FormateurId, motif: MotifRejet) -> None:
        """
        Reject the request (admin action)

        Business flow:
        1. Admin reviews request
        2. Admin rejects with reason
        3. Status changes to REJETEE
        4. Event raised to notify candidate

        Args:
            admin_id: ID of the admin who rejected
            motif: Reason for rejection (required)

        Raises:
            DemandeNonRejetableException: If not in EN_ATTENTE_VALIDATION
        """
        # Check business rule: can only reject if EN_ATTENTE
        if not self._statut.peut_etre_rejetee():
            raise DemandeNonRejetableException(self.id, self._statut)

        # Change state
        self._statut = StatutDemande.rejetee()
        self._motif_rejet = motif

        # Raise domain event
        self._record_event(
            DemandeCompteFormateurRejetee(
                demande_id=self.id,
                rejete_par_admin_id=admin_id,
                motif=motif,
            )
        )

    def ajouter_skill(self, skill: Skill) -> None:
        """
        Add a skill to the request (only if EN_ATTENTE)

        Business rule: Can only modify skills before validation/rejection

        Args:
            skill: Skill to add
        """
        if self._statut.est_finale():
            raise ValueError("Cannot modify a finalized request")

        self._skills.append(skill)

    def nombre_skills(self) -> int:
        """Get number of skills"""
        return len(self._skills)

    # ==================== DOMAIN EVENT MANAGEMENT ====================

    def _record_event(self, event) -> None:
        """
        Record a domain event (private method)

        Events are collected and will be published by infrastructure
        after the aggregate is saved.
        """
        self._events.append(event)

    def clear_events(self) -> None:
        """Clear all recorded events (called by infrastructure after publishing)"""
        self._events.clear()

    # ==================== REPRESENTATION ====================

    def __repr__(self) -> str:
        return (
            f"DemandeCompteFormateur("
            f"id={self.id}, "
            f"email={self._candidat_info.email}, "
            f"statut={self._statut}, "
            f"skills={len(self._skills)})"
        )
