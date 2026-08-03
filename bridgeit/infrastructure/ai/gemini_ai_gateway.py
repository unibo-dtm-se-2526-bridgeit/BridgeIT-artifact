"""Infrastructure Layer: Gemini adapter for the AIGateway port.

This module is the only place in the codebase that knows the Gemini SDK
exists. The application layer depends only on the AIGateway port (see
application/ports/ai_gateway.py) and never on this module directly.

Uses the google-genai SDK (the current, GA Google Gen AI SDK for
Python -- see https://ai.google.dev/gemini-api/docs/quickstart).
"""

from __future__ import annotations

import json
import os

from google import genai

from bridgeit.application.ports.ai_gateway import AIGateway, AIGatewayError
from bridgeit.domain.ai_analysis import AIAnalysis, QualityScore

# Default model: a fast, free-tier-friendly Gemini model. Revisit if rate
# limits become an issue -- see report.md for the free-tier comparison
# the professor asked for.
DEFAULT_MODEL = "gemini-2.0-flash"

_ANALYSIS_PROMPT = """You are a Requirements Engineering assistant. Analyse the \
following software requirement, written in natural language, and reply with \
ONLY a JSON object (no markdown fences, no extra text) with this exact shape:

{{
  "quality_indication": "ready_for_validation" or "needs_clarification",
  "issues": ["short string describing issue 1", "short string describing issue 2"]
}}

Use "needs_clarification" if the requirement is ambiguous, incomplete, or \
lacks a measurable acceptance criterion. Use "ready_for_validation" \
otherwise. If there are no issues, return an empty list for "issues".

Requirement:
\"\"\"{requirement_text}\"\"\"
"""


class GeminiAIGateway(AIGateway):
    """Concrete AIGateway implementation backed by the Gemini API."""

    def __init__(self, client: genai.Client | None = None, model: str = DEFAULT_MODEL) -> None:
        # Accepting an optional pre-built client (rather than only reading
        # GEMINI_API_KEY internally) is what makes this class testable
        # with a mocked client -- see the corresponding test module.
        self._client = client if client is not None else genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        self._model = model

    def analyse(self, requirement_text: str) -> AIAnalysis:
        prompt = _ANALYSIS_PROMPT.format(requirement_text=requirement_text)
        response = self._client.models.generate_content(model=self._model, contents=prompt)
        if response.text is None:
            raise AIGatewayError("Gemini returned an empty response.")
        return self._parse_response(response.text)

    @staticmethod
    def _parse_response(raw_text: str) -> AIAnalysis:
        try:
            data = json.loads(raw_text)
            quality_score = QualityScore(data["quality_indication"])
            issues: tuple[str, ...] = tuple(data.get("issues", []))
        except (json.JSONDecodeError, KeyError, ValueError) as error:
            raise AIGatewayError(
                f"Could not parse Gemini's response into a valid AIAnalysis: {error}"
            ) from error
        return AIAnalysis(quality_score=quality_score, issues=issues)
