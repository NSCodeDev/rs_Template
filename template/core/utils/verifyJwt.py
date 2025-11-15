import jwt
from jwt import PyJWTError

from config.settings import JWT_ALGORITHM, JWT_PUBLIC_KEY


def verify_jwt_token(token: str) -> dict | None:
    """
    Verify JWT token using public key.

    Args:
        token: JWT token string

    Returns:
        Decoded payload dict if valid, None if invalid
    """
    if not JWT_PUBLIC_KEY:
        raise ValueError("JWT_PUBLIC_KEY not configured")

    try:
        payload = jwt.decode(
            token,
            JWT_PUBLIC_KEY,
            algorithms=[JWT_ALGORITHM],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_iat": True,
            },
        )
        return payload
    except PyJWTError as e:
        print(f"JWT verification failed: {e}")
        return None


def get_user_from_token(token: str) -> dict | None:
    """
    Extract user information from JWT token.

    Args:
        token: JWT token string (with or without 'Bearer ' prefix)
    Returns:
        User info dict or None if invalid
    # Remove 'Bearer ' prefix if present
    """
    if token.startswith("Bearer "):
        token = token[7:]

    payload = verify_jwt_token(token)
    if not payload:
        return None

    return {
        "user_id": payload.get("user_id"),
        "email": payload.get("email"),
        "username": payload.get("username"),
        "tenant_id": payload.get("tenant_id"),
        "is_superuser": payload.get("is_superuser", False),
        "is_owner": payload.get("is_owner", False),
    }


# verify and extract user info example


def verify_and_extract_user(token: str):
    from rest_framework_simplejwt.exceptions import TokenError
    from rest_framework_simplejwt.tokens import AccessToken

    try:
        if token.startswith("Bearer "):
            token = token[7:]
        # Verify and decode token using simplejwt
        access_token = AccessToken(token)  # type: ignore

        # Extract user information from token claims
        user_info = {
            "user_id": access_token.get("user_id"),
            "email": access_token.get("email"),
            "username": access_token.get("username"),
            "tenant_id": access_token.get("tenant_id"),
            "is_superuser": access_token.get("is_superuser", False),
            "is_owner": access_token.get("is_owner", False),
        }

        return user_info

    except TokenError as e:
        print(f"Invalid token: {e}", flush=True)
        return None
    except Exception as e:
        print(f"Error extracting user from token: {e}", flush=True)
        return None
