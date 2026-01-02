from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fetal Plane Explorer"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/v1"

    # Cors
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Model defaults
    MODEL_PATH: str = "assets/models/fetal_plane_resnet18.onnx"
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
