"""Exception: au moins une compétence est requise"""

from src.domain.trainer.exceptions import TrainerAccountRequestException


class RequiredSkillsException(TrainerAccountRequestException):

    def __init__(self):
        super().__init__(
            "At least one skill is required to submit a trainer account request"
        )
