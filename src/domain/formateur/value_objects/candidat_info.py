"""CandidatInfo - Composite value object for candidate information"""

from src.domain.shared import ValueObject
from src.domain.formateur.value_objects import Email, FullName


class CandidatInfo(ValueObject):
    """
    CandidatInfo - Composite value object

    Groups all candidate personal information together.

    Characteristics:
    ✓ Immutable composite
    ✓ Groups related values
    ✓ Validated as a whole

    Why composite?
    - These values change together
    - They form a cohesive concept
    - Easier to pass around than 2 separate parameters
    """
    __slots__ = ('_full_name', '_email')

    def __init__(self, full_name: FullName, email: Email):
        """
        Create CandidatInfo.

        Args:
            full_name: Validated full name
            email: Validated email
        """
        object.__setattr__(self, '_full_name', full_name)
        object.__setattr__(self, '_email', email)

    @property
    def full_name(self) -> FullName:
        return self._full_name

    @property
    def email(self) -> Email:
        return self._email

    @staticmethod
    def create(
        first_name: str,
        last_name: str,
        email: str
    ) -> 'CandidatInfo':
        """
        Factory method - creates CandidatInfo from raw strings.

        Validates all fields during creation.
        """
        return CandidatInfo(
            full_name=FullName(first_name, last_name),
            email=Email(email)
        )

    def est_complet(self) -> bool:
        """
        Business rule: Check if candidate info is complete.

        Returns:
            True if all fields are present and valid
        """
        return (
            self._full_name is not None
            and self._email is not None
        )

    def __str__(self) -> str:
        return f"{self._full_name} ({self._email})"
