"""User entity for the MagicSquare domain."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    """Represents an immutable user in the domain layer.

    Attributes:
        user_id: Unique identifier for the user.
        name: Display name of the user.
        email: Email address of the user.
    """

    user_id: str
    name: str
    email: str

    def __post_init__(self) -> None:
        """Validate domain invariants right after initialization."""
        if not self.user_id.strip():
            raise ValueError("user_id must not be blank")

        if not self.name.strip():
            raise ValueError("name must not be blank")

        self._validate_email(self.email)

    def change_email(self, next_email: str) -> User:
        """Return a new user with updated email.

        Args:
            next_email: New email address to set.

        Returns:
            New immutable user instance with the updated email.

        Raises:
            ValueError: If the next email is invalid.
        """
        self._validate_email(next_email)
        return User(user_id=self.user_id, name=self.name, email=next_email)

    @staticmethod
    def _validate_email(email: str) -> None:
        """Validate email format with minimal domain constraints.

        Args:
            email: Email address candidate.

        Raises:
            ValueError: If email is blank or missing '@'.
        """
        if not email.strip():
            raise ValueError("email must not be blank")

        if "@" not in email:
            raise ValueError("email must contain '@'")
