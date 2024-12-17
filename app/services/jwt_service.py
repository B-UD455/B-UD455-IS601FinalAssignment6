'''
# app/services/jwt_service.py
from builtins import dict, str
import jwt
from datetime import datetime, timedelta
from settings.config import settings

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    # Convert role to uppercase before encoding the JWT
    if 'role' in to_encode:
        to_encode['role'] = to_encode['role'].upper()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def decode_token(token: str):
    try:
        decoded = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return decoded
    except jwt.PyJWTError:
        return None
    
    '''
    
# app/services/jwt_service.py
import jwt
from datetime import datetime, timedelta
from settings.config import settings
from typing import Optional, Union

def create_access_token(
    *, 
    data: dict, 
    expires_delta: Optional[timedelta] = None, 
    token_type: str = "access_token"
) -> str:
    """
    Creates a JWT access token with an expiration and additional claims.

    Args:
        data (dict): Payload data to encode in the JWT.
        expires_delta (Optional[timedelta]): Expiration duration for the token.
        token_type (str): The type of token being created (e.g., 'access_token').

    Returns:
        str: Encoded JWT string.
    """
    to_encode = data.copy()

    # Convert role to uppercase for standardization
    if "role" in to_encode:
        to_encode["role"] = to_encode["role"].upper()

    # Add expiration claim
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({
        "exp": expire,
        "token_type": token_type
    })

    # Encode the JWT
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def decode_token(token: str) -> Union[dict, None]:
    """
    Decodes a JWT token and validates its claims.

    Args:
        token (str): Encoded JWT string.

    Returns:
        dict: Decoded payload if the token is valid.
        None: If the token is invalid or expired.
    """
    try:
        decoded = jwt.decode(
            token, 
            settings.jwt_secret_key, 
            algorithms=[settings.jwt_algorithm]
        )
        return decoded
    except jwt.ExpiredSignatureError:
        # Handle token expiration
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        # Handle invalid token
        return {"error": "Invalid token"}


def is_token_valid(token: str, expected_role: Optional[str] = None) -> bool:
    """
    Validates the token and optionally checks if the role matches the expected role.

    Args:
        token (str): Encoded JWT string.
        expected_role (Optional[str]): The role to validate against.

    Returns:
        bool: True if the token is valid and role matches (if provided), else False.
    """
    decoded = decode_token(token)
    if not decoded or "error" in decoded:
        return False

    if expected_role and decoded.get("role") != expected_role.upper():
        return False

    return True

def generate_email_verification_token(user_id: int, expires_in_minutes: int = 60) -> str: #NEWCODE
    """
    Generates an email verification token.
    """
    expiration = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    payload = {"sub": str(user_id), "exp": expiration}
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token
