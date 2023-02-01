from pydantic import BaseSettings

# store the information in environment
class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_name: str
    database_user: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_min: int

    class Config:
        env_file = ".env"

settings = Settings()
