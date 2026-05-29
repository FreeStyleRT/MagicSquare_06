"""Boundary layer — input validation and response contracts."""

from src.boundary.contracts import FailureResponse
from src.boundary.validator import BoundaryValidator

__all__ = ["BoundaryValidator", "FailureResponse"]
