"""Domain layer package.

Contains the Requirement aggregate root and its value objects
(RequirementText, RequirementStatus), together with the business rules
and lifecycle transitions that govern them. See docs/domain-model.md
for the full conceptual description.

Per docs/architecture.md -- Dependency Rules, nothing in this package
may import from bridgeit.application, bridgeit.adapters, or
bridgeit.infrastructure, nor from any third-party framework (FastAPI,
SQLAlchemy, the Gemini SDK, etc.). This is what keeps the domain
independently testable and free of any infrastructure or
delivery-mechanism dependency -- the same principle that keeps the
root bridgeit/__init__.py's logging setup out of this file: logging
configuration is an application-level, cross-cutting concern, not a
domain one.
"""
