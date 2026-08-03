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
        # Deliberately NOT reading GEMINI_API_KEY here: constructing this
        # class (e.g. once at app startup, mirroring how _repository is
        # constructed in main.py) must never fail just because the key
        # isn't set yet -- that would take down the whole app (and any
        # test or CI run that imports main.py) over a single AI feature.
        # The key is only required once analyse() is actually called.
        self._client = client
        self._model = model

    def _get_client(self) -> genai.Client:
        if self._client is None:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                raise AIGatewayError(
                    "GEMINI_API_KEY is not set. Set it as an environment "
                    "variable before requesting an AI analysis."
                )
            self._client = genai.Client(api_key=api_key)
        return self._client

    def analyse(self, requirement_text: str) -> AIAnalysis:
        client = self._get_client()
        prompt = _ANALYSIS_PROMPT.format(requirement_text=requirement_text)
        response = client.models.generate_content(model=self._model, contents=prompt)
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
