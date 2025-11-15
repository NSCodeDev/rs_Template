"""Custom exception handlers for better API error responses"""

from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler that transforms DRF errors into a consistent format.

    Returns:
        {
            "error": {
                "code": "validation_error",
                "message": "Validation failed",
                "details": {
                    "field_name": ["error message"]
                }
            }
        }
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            "error": {
                "code": get_error_code(exc),
                "message": get_error_message(exc),
            }
        }

        # Handle different error formats
        if isinstance(response.data, dict):
            # Check for non_field_errors (common in authentication)
            if "non_field_errors" in response.data:
                # Convert non_field_errors to a more descriptive format
                errors = response.data["non_field_errors"]
                if isinstance(errors, list) and len(errors) > 0:
                    custom_response_data["error"]["message"] = errors[0]
                else:
                    custom_response_data["error"]["message"] = str(errors)

                # Remove non_field_errors and add remaining fields as details
                remaining_fields = {
                    k: v for k, v in response.data.items() if k != "non_field_errors"
                }
                if remaining_fields:
                    custom_response_data["error"]["details"] = remaining_fields
            else:
                # Add all field errors as details
                custom_response_data["error"]["details"] = response.data
        elif isinstance(response.data, list):
            # Handle list of errors
            custom_response_data["error"]["message"] = (
                response.data[0] if response.data else "An error occurred"
            )
        else:
            # Handle string or other formats
            custom_response_data["error"]["message"] = str(response.data)

        response.data = custom_response_data

    return response


def get_error_code(exc):
    """
    Determine error code based on exception type.
    """
    exception_name = exc.__class__.__name__

    error_code_mapping = {
        "ValidationError": "validation_error",
        "AuthenticationFailed": "authentication_failed",
        "NotAuthenticated": "not_authenticated",
        "PermissionDenied": "permission_denied",
        "NotFound": "not_found",
        "MethodNotAllowed": "method_not_allowed",
        "NotAcceptable": "not_acceptable",
        "UnsupportedMediaType": "unsupported_media_type",
        "Throttled": "throttled",
        "ParseError": "parse_error",
    }

    return error_code_mapping.get(exception_name, "error")


def get_error_message(exc):
    """
    Get a user-friendly error message based on exception type.
    """
    exception_name = exc.__class__.__name__

    default_messages = {
        "ValidationError": "Validation failed",
        "AuthenticationFailed": "Authentication failed",
        "NotAuthenticated": "Authentication credentials were not provided",
        "PermissionDenied": "You do not have permission to perform this action",
        "NotFound": "Resource not found",
        "MethodNotAllowed": "Method not allowed",
        "NotAcceptable": "Not acceptable",
        "UnsupportedMediaType": "Unsupported media type",
        "Throttled": "Request was throttled",
        "ParseError": "Malformed request",
    }

    return default_messages.get(exception_name, "An error occurred")
