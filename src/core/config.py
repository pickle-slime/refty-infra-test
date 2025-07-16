from datetime import datetime
from dataclasses import dataclass, field
from dotenv import load_dotenv
from pathlib import Path
import os

@dataclass
class Settings:
    PROJECT_NAME: str = "refty-infra-test"
    API_V1_PREFIX: str = "/api/v1"

    START_TIME: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self.env = self.Environment()

    class Environment:
        def __init__(self, env_path: str = ".env"):
            abs_path = Path(env_path).resolve()
            load_dotenv(dotenv_path=abs_path)

        @staticmethod
        def get_variable(name: str) -> str | None:
            return os.getenv(name)

settings = Settings()

