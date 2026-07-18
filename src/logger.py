import logging
import json
import sys
from datetime import datetime, timezone
from typing import Any

class JsonFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    Converts log records to JSON format for easy parsing in AWS CloudWatch.
    """
    def format(self, record: logging.LogRecord) -> str:
        # Create a dictionary with core log fields
        log_data: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Include exception tracebacks if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            
        # Merge extra properties if passed to the log
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)  # type: ignore
            
        return json.dumps(log_data)

def get_logger(name: str) -> logging.Logger:
    """
    Configures and returns a structured JSON logger.
    
    Args:
        name: Name of the logger.
        
    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if logger is re-initialized
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        
    # Prevent propagation to root logger to avoid double logging in Lambda
    logger.propagate = False
    return logger
