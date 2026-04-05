"""Application configuration loaded from environment variables."""

import os


class Settings:
    app_env: str = os.getenv("APP_ENV", "development")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    service_name: str = os.getenv("SERVICE_NAME", "cicd-pipeline-demo")
    service_version: str = os.getenv("SERVICE_VERSION", "0.1.0")

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


settings = Settings()
