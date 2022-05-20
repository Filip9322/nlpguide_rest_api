from pydantic import BaseSettings


class Settings(BaseSettings):
    env_file = '.env'
    env_file_encoding = 'utf-8'
    app_name: str = "NLPGuide"
    admin_email: str


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
