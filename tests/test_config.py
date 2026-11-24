import pytest
from pydantic import ValidationError

from ai_project_skeleton.config import Settings


def test_settings_load_environment_variables(monkeypatch):
    monkeypatch.setenv("APP_BASE_URL", "https://test.example.com")
    monkeypatch.setenv("APP_TIMEOUT_SECONDS", "20")
    monkeypatch.setenv("APP_MAX_RETRIES", "5")

    settings = Settings(_env_file=None)

    assert settings.base_url == "https://test.example.com"
    assert settings.timeout_seconds == 20
    assert settings.max_retries == 5


def test_settings_reject_invalid_timeout():
    with pytest.raises(ValidationError):
        Settings(timeout_seconds=0)
