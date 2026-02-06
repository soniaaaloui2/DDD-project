"""Event: La demande de compte formateur a été soumise"""

from datetime import datetime
from src.domain.trainer.value_objects import RequestId, Email


class TrainerAccountRequestSubmitted:

    def __init__(
        self,
        request_id: RequestId,
        candidate_email: Email,
        occurred_on: datetime = None
    ):
        self.request_id = request_id
        self.candidate_email = candidate_email
        self.occurred_on = occurred_on or datetime.now()

    def __repr__(self) -> str:
        return (
            f"TrainerAccountRequestSubmitted("
            f"request_id={self.request_id}, "
            f"candidate_email={self.candidate_email}, "
            f"occurred_on={self.occurred_on})"
        )
