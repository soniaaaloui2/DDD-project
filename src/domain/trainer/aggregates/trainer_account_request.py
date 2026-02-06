"""TrainerAccountRequest - Point d'entrée de l'agrégat pour la demande de compte formateur"""

from datetime import datetime
from typing import List

from domain.shared import Entity
from domain.trainer.value_objects import (
    RequestId,
    Email,
    RequestStatus,
    CandidatInfo,
)
from domain.trainer.entities import Skill
from domain.trainer.events import (
    TrainerAccountRequestSubmitted,
)
from domain.trainer.exceptions import (
    RequiredSkillsException,
)


class TrainerAccountRequest(Entity[RequestId]):

    def __init__(
        self,
        request_id: RequestId,
        candidate_info: CandidatInfo,
        skills: List[Skill],
        status: RequestStatus,
        submission_date: datetime,
    ):
        super().__init__(request_id)

        if not skills:
            raise RequiredSkillsException()

        self._candidate_info = candidate_info
        self._skills = list(skills)
        self._status = status
        self._submission_date = submission_date

        self._events: List = []

    @property
    def candidate_info(self) -> CandidatInfo:
        return self._candidate_info

    @property
    def skills(self) -> List[Skill]:
        return list(self._skills)

    @property
    def statut(self) -> RequestStatus:
        return self._status

    @property
    def submission_date(self) -> datetime:
        return self._submission_date


    @property
    def events(self) -> List:
        return list(self._events)


    @staticmethod
    def submit(
        candidate_info: CandidatInfo,
        skills: List[Skill]
    ) -> 'TrainerAccountRequest':

        if not skills:
            raise RequiredSkillsException()

        # Create the aggregate
        request = TrainerAccountRequest(
            request_id=RequestId.generate(),
            candidate_info=candidate_info,
            skills=skills,
            status=RequestStatus.pending_validation(),
            submission_date=datetime.now(),
        )

        request._record_event(
            TrainerAccountRequestSubmitted(
                request_id=request.id,
                candidate_email=candidate_info.email,
            )
        )

        return request

    # gestion des evenements domaine
    def _record_event(self, event) -> None:
        self._events.append(event)

    def clear_events(self) -> None:
        self._events.clear()


    def __repr__(self) -> str:
        return (
            f"TrainerAccountRequest("
            f"id={self.id}, "
            f"email={self._candidate_info.email}, "
            f"status={self._status}, "
            f"skills={len(self._skills)})"
        )
