import logging
import threading
import uuid

logger = logging.getLogger(__name__)

_thread_locals = threading.local()


def get_current_tenant():
    """Get the current tenant from thread-local storage."""
    return getattr(_thread_locals, "tenant", None)


def get_current_user():
    """Get the current user from thread-local storage."""
    return getattr(_thread_locals, "user", None)


def get_current_tenant_id():
    """Get the current tenant ID from thread-local storage."""
    return getattr(_thread_locals, "tenant_id", None)


def get_request_id():
    """Get the current request ID from thread-local storage."""
    return getattr(_thread_locals, "request_id", None)


def _set_thread_locals(tenant=None, user=None, tenant_id=None, request_id=None):
    """Set thread-local variables."""
    if tenant is not None:
        _thread_locals.tenant = tenant
    if user is not None:
        _thread_locals.user = user
    if tenant_id is not None:
        _thread_locals.tenant_id = tenant_id
    if request_id is not None:
        _thread_locals.request_id = request_id


def _clear_thread_locals():
    """Clear all thread-local variables to prevent memory leaks."""
    for attr in ["tenant", "user", "tenant_id", "request_id"]:
        try:
            delattr(_thread_locals, attr)
        except AttributeError:
            pass


class TenantAwareMiddleware:
    """
    Middleware to set the current tenant based on JWT token in request headers.
    Automatically cleans up thread-local storage after request processing.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            logger.info(
                f"[MIDDLEWARE] Processing request: {request.method} {request.path}"
            )

            # skip middleware for some paths
            from config.settings import SKIP_PATHS

            if request.path in SKIP_PATHS:
                logger.info(
                    f"[MIDDLEWARE] Skipping middleware for path: {request.path}"
                )
                return self.get_response(request)

            # Generate unique request ID for tracing
            request_id = uuid.uuid4()
            request.request_id = request_id
            _set_thread_locals(request_id=request_id)
            logger.info(f"[MIDDLEWARE] Request ID: {request_id}")

            # Try to get user info from JWT token first (API requests)
            auth_header = request.headers.get("Authorization", "")
            logger.info(
                f"[MIDDLEWARE] Authorization header present: {bool(auth_header)}"
            )

            user_info = None

            # Try JWT authentication first
            if auth_header:
                user_info = self._get_user_from_token(request)
                if user_info:
                    logger.info(f"[MIDDLEWARE] User authenticated via JWT")

            # Fallback to session authentication (Django admin)
            if (
                not user_info
                and hasattr(request, "user")
                and request.user
                and request.user.is_authenticated
            ):
                user_info = self._get_user_from_session(request)
                if user_info:
                    logger.info(f"[MIDDLEWARE] User authenticated via session/cookie")

            if user_info:
                tenant_id = user_info.get("tenant_id")

                # Set request attributes
                request.tenant_id = tenant_id
                request.user_info = user_info

                # Set thread-local variables
                _set_thread_locals(
                    tenant=user_info, user=user_info, tenant_id=tenant_id
                )

                logger.info(
                    f"[MIDDLEWARE] Tenant {tenant_id} authenticated for user {user_info.get('email')}"
                )
            else:
                logger.warning(f"[MIDDLEWARE] No valid tenant/user information found")

            # Process request
            response = self.get_response(request)

            return response

        finally:
            # Always clean up thread-local storage to prevent memory leaks
            _clear_thread_locals()

    def _get_user_from_token(self, request):
        """
        Extract and verify user information from JWT token in Authorization header.

        Returns:
            dict: User information if token is valid, None otherwise
        """
        from core.util.verifyJwt import verify_and_extract_user

        auth_header = request.headers.get("Authorization", "")

        if not auth_header.startswith("Bearer "):
            return None

        try:
            user_info = verify_and_extract_user(auth_header)
            return user_info
        except (ValueError, KeyError) as e:
            logger.warning("Failed to extract user from token: %s", str(e))
            return None

    def _get_user_from_session(self, request):
        """
        Extract user information from Django session (for admin and session-based auth).

        Returns:
            dict: User information if session user is valid, None otherwise
        """
        try:
            user = request.user

            if not user or not user.is_authenticated:
                return None

            # Build user info dict similar to JWT payload
            user_info = {
                "user_id": str(user.id),
                "email": user.email,
                "username": user.username,
                "is_superuser": user.is_superuser,
                "is_staff": user.is_staff,
                "is_active": user.is_active,
                "is_owner": getattr(user, "is_owner", False),
            }

            # Add tenant_id if user has it
            if hasattr(user, "tenant_id") and user.tenant_id:
                user_info["tenant_id"] = str(user.tenant_id)

            return user_info

        except Exception as e:
            logger.warning("Failed to extract user from session: %s", str(e))
            return None
