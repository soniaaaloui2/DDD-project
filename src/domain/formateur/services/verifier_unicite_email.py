"""Domain Service: Verify email uniqueness across aggregates"""

from src.domain.formateur.exceptions.email_deja_utilise_exception import EmailDejaUtiliseException
from src.domain.formateur.value_objects import Email
from src.domain.formateur.repositories import DemandeCompteFormateurRepositoryInterface
from src.domain.formateur.exceptions import DemandeCompteFormateurException


class VerifierUniciteEmail:
    """
    Domain Service: Verify email uniqueness

    Why a Domain Service? (from course)
    ✓ Operation requires data beyond a single aggregate
    ✓ Dependencies stay within the same Bounded Context
    ✓ Operation is a business concept itself
    ✓ Stateless (no internal state)

    Business Rule:
    An email can only be used in ONE active request at a time.
    - Active = EN_ATTENTE_VALIDATION or VALIDEE
    - Rejected requests don't count (candidate can resubmit)

    Usage:
```python
    verifier = VerifierUniciteEmail(demande_repo)
    verifier.execute(Email("test@example.com"))  # Raises if already used
```

    Characteristics (from course):
    ✓ Stateless: No internal state
    ✓ Business operation: Expresses domain action
    ✓ Named with verb: VerifierUniciteEmail
    ✓ Same Bounded Context: Dependencies in Formateur domain
    """

    def __init__(
        self,
        demande_repository: DemandeCompteFormateurRepositoryInterface
    ):
        """
        Initialize the service with its dependencies.

        Args:
            demande_repository: Repository to check existing requests
        """
        self._demande_repository = demande_repository

    def execute(self, email: Email) -> None:
        """
        Verify that email is not already used.

        Business logic:
        - Check if email exists in any active request
        - Active = EN_ATTENTE_VALIDATION or VALIDEE
        - Rejected requests are ignored (can resubmit)

        Args:
            email: Email to verify

        Raises:
            EmailDejaUtiliseException: If email already exists

        Example:
```python
        try:
            verifier.execute(Email("john@example.com"))
            # Email is available
        except EmailDejaUtiliseException:
            # Email already used
```
        """
        # Check if email exists
        if self._demande_repository.exists_by_email(email):
            raise EmailDejaUtiliseException(email)

    def est_disponible(self, email: Email) -> bool:
        """
        Check if email is available (non-throwing version).

        Convenience method that returns a boolean instead of raising.

        Args:
            email: Email to check

        Returns:
            True if email is available, False otherwise

        Example:
```python
        if verifier.est_disponible(Email("john@example.com")):
            # Email available
        else:
            # Email already used
```
        """
        try:
            self.execute(email)
            return True
        except EmailDejaUtiliseException:
            return False
