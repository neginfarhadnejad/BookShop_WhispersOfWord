from pydantic_settings import BaseSettings
from pydantic import Field ,BaseModel

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
