"""Application layer port: AIGateway.

Abstract interface between the application layer and any concrete AI
provider. Consistent with architecture.md -- AI Architecture: the
application layer depends only on this abstraction, never on a specific
AI provider's SDK. The concrete Gemini implementation lives in
infrastructure/ai/, the only place in the codebase allowed to import
the Gemini SDK.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from bridgeit.domain.ai_analysis import AIAnalysis


class AIGateway(ABC):
    """Port for requesting an AI-assisted analysis of a requirement's text."""

    @abstractmethod
    def analyse(self, requirement_text: str) -> AIAnalysis:
        """Analyse the given requirement text and return an AIAnalysis.

        Implementations should raise AIGatewayError (or a subclass) if
        the provider's response cannot be turned into a valid AIAnalysis
        -- callers should not need to know about provider-specific
        failure modes.
        """


class AIGatewayError(Exception):
    """Raised when an AIGateway implementation cannot produce a valid
    AIAnalysis (e.g. the provider's response is malformed or empty)."""
