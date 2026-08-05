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
import time

from google import genai
from google.genai import errors as genai_errors

from bridgeit.application.ports.ai_gateway import AIGateway, AIGatewayError
from bridgeit.domain.ai_analysis import AIAnalysis, QualityScore

# Default model: chosen from the models actually showing a non-zero
# free-tier quota on this project's AI Studio dashboard (checked
# 2026-08-03) -- "gemini-2.0-flash" itself showed 0/0/0 (deprecated in
# favour of newer versions), while the "flash-lite" variants had real,
# generous quotas. "gemini-3.5-flash-lite" had the highest daily limit
# (500 requests/day) among them, comfortably enough for course-project
# use, and "lite" is a good fit for this simple classification task
# (no need for a heavier full "Pro"/"Flash" model). If this exact model
# ID ever stops working, check aistudio.google.com's rate-limits page
# for whichever "flash-lite" model currently shows a non-zero quota.
DEFAULT_MODEL = "gemini-3.5-flash-lite"

# Retry policy for transient overload errors only (the professor's own
# forum message flagged free-tier rate limits as a real risk to plan
# for). Deliberately simple: a fixed number of attempts with a fixed
# short wait, not a full exponential-backoff/model-fallback system --
# that would be complexity this project hasn't actually needed yet.
_RETRYABLE_STATUS_CODES = frozenset({429, 503})
_MAX_ATTEMPTS = 3
_RETRY_DELAY_SECONDS = 1.5

_ANALYSIS_PROMPT = """You are a Requirements Engineering assistant helping a Business \
team member (not a software engineer) write better requirements. Analyse the \
following software requirement, written in natural language, and reply with \
ONLY a JSON object (no markdown fences, no extra text) with this exact shape:

{{
  "quality_indication": "ready_for_validation" or "needs_clarification",
  "issues": ["issue 1: what's missing, and why it matters", "issue 2: ..."]
}}

Use "needs_clarification" if the requirement is ambiguous, incomplete, or \
lacks a measurable acceptance criterion. Use "ready_for_validation" \
otherwise. If there are no issues, return an empty list for "issues".

Each issue must teach, not just flag: briefly explain not only what is \
missing, but why it matters for building the right thing (e.g. why an \
actor, a measurable condition, or a scope boundary makes the requirement \
usable) -- in plain language a non-technical reader can learn from, not \
Software Engineering jargon.

Requirement:
\"\"\"{requirement_text}\"\"\"
"""


class GeminiAIGateway(AIGateway):
    """Concrete AIGateway implementation backed by the Gemini API."""

    def __init__(
        self, client: genai.Client | None = None, model: str = DEFAULT_MODEL
    ) -> None:
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
        response = self._generate_with_retry(client, self._model, prompt)
        if response.text is None:
            raise AIGatewayError("Gemini returned an empty response.")
        return self._parse_response(response.text)

    @staticmethod
    def _generate_with_retry(
        client: genai.Client, model: str, prompt: str
    ) -> genai.types.GenerateContentResponse:
        """Calls Gemini, retrying only on transient overload errors
        (429 rate-limited, 503 temporarily unavailable) with a short
        wait between attempts. Any other error (e.g. 401 invalid key,
        404 unknown model) is not retryable and fails immediately --
        retrying those would just waste time on a guaranteed failure.
        """
        for attempt in range(1, _MAX_ATTEMPTS + 1):
            try:
                return client.models.generate_content(model=model, contents=prompt)
            except genai_errors.APIError as error:
                is_retryable = error.code in _RETRYABLE_STATUS_CODES
                is_last_attempt = attempt == _MAX_ATTEMPTS
                if not is_retryable or is_last_attempt:
                    raise AIGatewayError(f"Gemini API error: {error}") from error
                time.sleep(_RETRY_DELAY_SECONDS)
        # Unreachable: the loop above always returns or raises. Present
        # only to satisfy mypy that this function has no implicit
        # "falls off the end and returns None" path.
        raise AssertionError("unreachable")

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
