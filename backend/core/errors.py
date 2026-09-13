from typing import Any, Dict, Optional
import os

class APIError(Exception):
    """
    Base class for all API exceptions. 
    Framework-agnostic but designed to be caught by a global exception handler.
    """
    def __init__(
        self, 
        code: str, 
        message: str, 
        status_code: int = 400, 
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the error to the standardized API response format."""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details
            }
        }


# --- Specific Application Errors ---

class InvalidFileError(APIError):
    def __init__(self, message: str = "The provided file is invalid or corrupted.", details: Optional[Dict[str, Any]] = None):
        super().__init__(code="INVALID_FILE", message=message, status_code=400, details=details)

class UnsupportedFormatError(APIError):
    def __init__(self, message: str = "The provided file format is not supported.", details: Optional[Dict[str, Any]] = None):
        super().__init__(code="UNSUPPORTED_FORMAT", message=message, status_code=415, details=details)

class MissingMetadataError(APIError):
    def __init__(self, message: str = "Required metadata is missing from the dataset.", details: Optional[Dict[str, Any]] = None):
        super().__init__(code="MISSING_METADATA", message=message, status_code=400, details=details)

class IncompatibleImagePairsError(APIError):
    def __init__(self, message: str = "The provided image pairs are incompatible (e.g. mismatched dimensions, CRS, or bounds).", details: Optional[Dict[str, Any]] = None):
        super().__init__(code="INCOMPATIBLE_IMAGE_PAIRS", message=message, status_code=400, details=details)

class ModelUnavailableError(APIError):
    def __init__(self, message: str = "The requested AI model is currently unavailable.", details: Optional[Dict[str, Any]] = None):
        super().__init__(code="MODEL_UNAVAILABLE", message=message, status_code=503, details=details)

class GISProcessingFailureError(APIError):
    def __init__(self, message: str = "A failure occurred during GIS data processing.", details: Optional[Dict[str, Any]] = None):
        super().__init__(code="GIS_PROCESSING_FAILURE", message=message, status_code=500, details=details)


# --- Framework Integration Helpers ---

def format_unexpected_error(exc: Exception) -> Dict[str, Any]:
    """
    Helper to safely format unexpected 500 errors.
    Ensures internal stack traces and secrets are NOT exposed in production.
    """
    environment = os.getenv("ENVIRONMENT", "production").lower()
    
    error_response = {
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected server error occurred.",
            "details": {}
        }
    }

    # Only attach actual exception details if we are explicitly in development
    if environment in ["development", "local", "dev"]:
        error_response["error"]["details"]["exception"] = str(exc)
        error_response["error"]["details"]["type"] = type(exc).__name__
        
    return error_response
