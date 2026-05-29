"""Boundary layer — input validation and response contracts."""

from src.boundary.contracts import FailureResponse
from src.boundary.error_mapper import ErrorMapper
from src.boundary.validator import BoundaryValidator

__all__ = ["BoundaryValidator", "ErrorMapper", "FailureResponse"]
