"""Boundary layer — input validation and response contracts."""

from magic_square.boundary.contracts import FailureResponse
from magic_square.boundary.validator import BoundaryValidator

__all__ = ["BoundaryValidator", "FailureResponse"]
