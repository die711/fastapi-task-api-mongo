from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_ALGORITHM: str
    MONGO_URL: str

    class Config:
        env_file = '.env'
