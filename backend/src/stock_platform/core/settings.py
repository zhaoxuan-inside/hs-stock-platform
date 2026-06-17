from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "hs-stock-platform"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = False

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_db: str = "stock_platform"

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""

    mongodb_host: str = "localhost"
    mongodb_port: int = 27017
    mongodb_db: str = "stock_platform"

    etcd_host: str = "localhost"
    etcd_port: int = 2379

    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    @property
    def mongodb_url(self) -> str:
        return f"mongodb://{self.mongodb_host}:{self.mongodb_port}/"


settings = Settings()