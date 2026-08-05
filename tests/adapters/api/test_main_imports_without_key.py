"""Confirms that importing main.py never fails just because
GEMINI_API_KEY isn't set -- constructing the AI Gateway at startup must
be safe regardless (see gemini_ai_gateway.py's lazy client creation).
"""

import importlib


def test_main_module_imports_successfully_without_gemini_api_key(
    monkeypatch: "object",
) -> None:
    import pytest

    mp = pytest.MonkeyPatch()
    mp.delenv("GEMINI_API_KEY", raising=False)
    try:
        import bridgeit.adapters.api.main as main_module

        importlib.reload(main_module)
        assert main_module.app is not None
    finally:
        mp.undo()
