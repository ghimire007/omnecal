from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT

SECRET_KEY = "e8oorj8)y+h#jn-j!@wmyyr)z)xzh3vj80os^$29f)_txkh)"
PASSWORD_HASH_ROUNDS = 12


class jwtSettings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY
    authjwt_access_token_expires: int = 3600 * 2


@AuthJWT.load_config
def get_config():
    return jwtSettings()
