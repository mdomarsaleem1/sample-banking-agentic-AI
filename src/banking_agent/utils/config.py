"""
Configuration management for the banking agent.
"""

import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv


class Config(BaseModel):
    """Application configuration."""

    # AI Provider settings
    ai_provider: str = "mock"
    ai_model: str = "mock-model"
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # API simulation settings
    api_latency_min_ms: int = 50
    api_latency_max_ms: int = 200

    # Logging
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        load_dotenv()

        return cls(
            ai_provider=os.getenv("AI_PROVIDER", "mock"),
            ai_model=os.getenv("AI_MODEL", "mock-model"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            api_latency_min_ms=int(os.getenv("API_LATENCY_MIN_MS", "50")),
            api_latency_max_ms=int(os.getenv("API_LATENCY_MAX_MS", "200")),
            log_level=os.getenv("LOG_LEVEL", "INFO")
        )


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config.from_env()
    return _config


def reset_config():
    """Reset the global configuration (useful for testing)."""
    global _config
    _config = None
