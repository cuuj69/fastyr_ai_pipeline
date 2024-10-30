import logging
import structlog
from typing import Dict, Any
import json_log_formatter
import sys

class CustomJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message: str, extra: Dict[str, Any], record: logging.LogRecord) -> Dict[str, Any]:
        extra['message'] = message
        extra['level'] = record.levelname
        extra['timestamp'] = self.format_timestamp(record.created)
        
        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)
            
        return extra

def setup_logging(log_level: str = "INFO") -> None:
    """Configure structured logging with JSON output."""
    
    # Configure standard logging
    json_handler = logging.StreamHandler(sys.stdout)
    json_handler.setFormatter(CustomJSONFormatter())
    
    logging.basicConfig(
        level=log_level,
        handlers=[json_handler]
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(log_level)),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True
    ) 