"""Application layer errors shared by more than one use case."""


class RequirementNotFoundError(Exception):
    """Raised when no Requirement exists with the given id."""
