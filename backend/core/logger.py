import logging
import json
import os
from datetime import datetime, timezone
import traceback
from typing import Any, Dict, Optional

class StructuredJSONFormatter(logging.Formatter):
    """
    A custom JSON formatter for structured logging.
    Ensures standard fields and parses extra attributes gracefully.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "component": getattr(record, "component", "system"),
        }
        
        # Standard structural fields requested
        optional_fields = [
            "job_id", 
            "request_id", 
            "operation", 
            "status", 
            "duration"
        ]
        
        for field in optional_fields:
            if hasattr(record, field):
                log_record[field] = getattr(record, field)

        # Handle errors and exceptions natively
        if record.exc_info:
            log_record["error"] = self.formatException(record.exc_info)
        elif hasattr(record, "error") and record.error:
            log_record["error"] = str(record.error)

        return json.dumps(log_record)

def setup_logger(name: str = "satquery") -> logging.Logger:
    """
    Sets up the root logger with the structured JSON formatter.
    Respects the LOG_LEVEL environment variable.
    """
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Avoid duplicate handlers if setup_logger is called multiple times
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(StructuredJSONFormatter())
        logger.addHandler(console_handler)
        
    return logger

class StructuredLogger(logging.LoggerAdapter):
    """
    A LoggerAdapter to easily inject standard structured fields.
    """
    def process(self, msg: Any, kwargs: Any) -> tuple[Any, Dict[str, Any]]:
        extra = kwargs.get("extra", {})
        
        # Combine adapter's extra context with method-specific extra kwargs
        merged_extra = {**self.extra, **extra}
        
        # NOTE: Be extremely careful NOT to pass raw user inputs/PII directly into extra dicts
        # PII filtering/sanitization logic can be expanded here in the future
        
        kwargs["extra"] = merged_extra
        return msg, kwargs

def get_logger(component: str) -> StructuredLogger:
    """
    Factory function to retrieve a context-aware structured logger.
    
    Usage:
        logger = get_logger("auth_service")
        logger.info("User logged in", extra={"request_id": "123", "duration": 45, "status": "success"})
    """
    base_logger = setup_logger()
    return StructuredLogger(base_logger, {"component": component})
