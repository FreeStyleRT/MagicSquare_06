"""Control layer — use-case orchestration between Boundary and Domain."""

from magic_square.control.domain_resolver import DomainResolver
from magic_square.control.resolve_use_case import ResolveUseCase

__all__ = ["DomainResolver", "ResolveUseCase"]
