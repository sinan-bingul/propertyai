import pytest


@pytest.fixture(autouse=True)
def _dummy_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy")
