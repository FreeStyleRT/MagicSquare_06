"""User entity tests following AAA pattern."""

import pytest

from magic_square.entity.user import User


def test_create_user_with_valid_values() -> None:
    """Create a user successfully when all values are valid."""
    # Arrange
    user_id = "user-001"
    name = "Alice"
    email = "alice@example.com"

    # Act
    user = User(user_id=user_id, name=name, email=email)

    # Assert
    assert user.user_id == user_id
    assert user.name == name
    assert user.email == email


def test_create_user_raises_for_blank_name() -> None:
    """Raise ValueError when user name is blank."""
    # Arrange
    user_id = "user-002"
    blank_name = "   "
    email = "alice@example.com"

    # Act / Assert
    with pytest.raises(ValueError, match="name must not be blank"):
        User(user_id=user_id, name=blank_name, email=email)


def test_create_user_raises_for_invalid_email() -> None:
    """Raise ValueError when email format is invalid."""
    # Arrange
    user_id = "user-003"
    name = "Alice"
    invalid_email = "alice-at-example.com"

    # Act / Assert
    with pytest.raises(ValueError, match="email must contain '@'"):
        User(user_id=user_id, name=name, email=invalid_email)


def test_change_email_returns_new_user_with_updated_email() -> None:
    """Return a new user with changed email."""
    # Arrange
    user = User(user_id="user-004", name="Alice", email="alice@example.com")
    next_email = "alice.next@example.com"

    # Act
    updated = user.change_email(next_email)

    # Assert
    assert updated.email == next_email
    assert updated.user_id == user.user_id
    assert updated.name == user.name
    assert updated is not user


def test_change_email_raises_for_invalid_email() -> None:
    """Raise ValueError when changing email to invalid value."""
    # Arrange
    user = User(user_id="user-005", name="Alice", email="alice@example.com")
    invalid_email = "alice.example.com"

    # Act / Assert
    with pytest.raises(ValueError, match="email must contain '@'"):
        user.change_email(invalid_email)
