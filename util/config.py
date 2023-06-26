from enum import Enum
from pydantic import BaseSettings
import redis

from util.api_secrets import get_secret

keys = get_secret()

redis_cache = redis.Redis(
    host = keys["redis_host"],
    port = 11929,
    password = keys["redis_password"],
)

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50

    class Config:
        env_file = ".env"

# settings = Settings()

class Tags(Enum):
    leads = "Leads"
    users = "users"
    emails = "Emails"
