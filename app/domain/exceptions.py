class DomainError(Exception):
    """Base error for expected business rule failures."""


class InvalidEntityError(DomainError):
    """An entity violates a domain invariant."""


class InspectionRejectedError(DomainError):
    """A vehicle did not pass the service-center inspection."""


class DuplicateInventoryNumberError(DomainError):
    """An inventory number is already registered."""
