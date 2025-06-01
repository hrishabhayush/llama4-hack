import os
from pathlib import Path
from dotenv import load_dotenv
from enum import Enum
from typing import Optional, Dict, Any
from .db_log import setup_logger

# Get logger for this module
logger = setup_logger(__name__)

class EnvErrorType(Enum):
    """Enumeration of possible environment error types"""
    MISSING_FILE = "missing_env_file"
    MISSING_VARIABLE = "missing_variable"
    INVALID_VALUE = "invalid_value"
    PERMISSION_ERROR = "permission_error"
    UNKNOWN = "unknown_error"

class EnvironmentError(Exception):
    """
    Custom exception for environment configuration errors.
    
    Attributes:
        error_type: Type of environment error (from EnvErrorType enum)
        message: Human-readable error message
        details: Additional error details (e.g., missing variable names)
        suggestion: Suggested fix for the error
    """
    def __init__(
        self,
        error_type: EnvErrorType,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        suggestion: Optional[str] = None
    ):
        self.error_type = error_type
        self.message = message
        self.details = details or {}
        self.suggestion = suggestion
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """Format the error message with details and suggestion"""
        error_msg = f"[{self.error_type.value}] {self.message}"
        
        if self.details:
            error_msg += f"\nDetails: {self.details}"
        
        if self.suggestion:
            error_msg += f"\nSuggestion: {self.suggestion}"
        
        return error_msg

def _validate_log_level(value: str) -> bool:
    """Validate log level value"""
    return value.upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

def _validate_memory_limit(value: str) -> bool:
    """Validate memory limit value"""
    try:
        limit = int(value)
        return limit > 0
    except ValueError:
        return False

def _validate_url(value: str) -> bool:
    """Validate URL format"""
    return value.startswith(('http://', 'https://'))

def _validate_chunk_size(value: str) -> bool:
    """Validate chunk size value"""
    try:
        size = int(value)
        return size > 0
    except ValueError:
        return False

def _validate_cluster_count(value: str) -> bool:
    """Validate cluster count value"""
    try:
        count = int(value)
        return count > 1  # Clustering requires at least 2 clusters
    except ValueError:
        return False

def check_environment() -> None:
    """
    Check if all required environment variables are set and valid.
    Raises EnvironmentError if any validation fails.
    """
    logger.info("Checking environment configuration...")
    
    # Check for .env file
    env_path = Path(__file__).parent.parent / '.env'
    if not env_path.exists():
        raise EnvironmentError(
            error_type=EnvErrorType.MISSING_FILE,
            message="Missing .env file in backend directory.",
            suggestion="Create a .env file based on .env.example"
        )
    
    try:
        load_dotenv(dotenv_path=env_path)
    except Exception as e:
        raise EnvironmentError(
            error_type=EnvErrorType.PERMISSION_ERROR,
            message="Could not load .env file",
            details={"original_error": str(e)},
            suggestion="Check file permissions and format"
        )
    
    # Get debug mode first as it affects which variables are required
    debug_mode = os.getenv('DEBUG', 'true').lower()
    if debug_mode not in ['true', 'false']:
        raise EnvironmentError(
            error_type=EnvErrorType.INVALID_VALUE,
            message="Invalid DEBUG value",
            details={"DEBUG": debug_mode},
            suggestion="Set DEBUG to 'true' or 'false'"
        )
    
    # Define validation rules for environment variables
    env_rules = {
        'DEBUG': {
            'required': True,
            'validator': lambda x: x.lower() in ['true', 'false'],
            'error_msg': "DEBUG must be 'true' or 'false'"
        },
        'QDRANT_URL': {
            'required': lambda: debug_mode == 'false',
            'validator': _validate_url,
            'error_msg': "QDRANT_URL must be a valid HTTP/HTTPS URL"
        },
        'QDRANT_API_KEY': {
            'required': False,  # Optional even in production
            'validator': lambda x: bool(x and len(x) > 0),
            'error_msg': "QDRANT_API_KEY cannot be empty if provided"
        },
        'MEMORY_LIMIT_GB': {
            'required': False,
            'validator': _validate_memory_limit,
            'error_msg': "MEMORY_LIMIT_GB must be a positive integer"
        },
        'GPU_MEMORY_LIMIT': {
            'required': False,
            'validator': _validate_memory_limit,
            'error_msg': "GPU_MEMORY_LIMIT must be a positive integer"
        },
        'LOG_LEVEL': {
            'required': False,
            'validator': _validate_log_level,
            'error_msg': "LOG_LEVEL must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"
        },
        'MIN_CHUNK_SIZE': {
            'required': True,
            'validator': _validate_chunk_size,
            'error_msg': "MIN_CHUNK_SIZE must be a positive integer"
        },
        'MAX_CHUNK_SIZE': {
            'required': True,
            'validator': lambda x: _validate_chunk_size(x) and int(x) > int(os.getenv('MIN_CHUNK_SIZE', '0')),
            'error_msg': "MAX_CHUNK_SIZE must be a positive integer greater than MIN_CHUNK_SIZE"
        },
        'MAX_WORKERS_PER_CHUNK': {
            'required': True,
            'validator': _validate_chunk_size,
            'error_msg': "MAX_WORKERS_PER_CHUNK must be a positive integer"
        },
        'K_MEANS_CLUSTERS': {
            'required': True,
            'validator': _validate_cluster_count,
            'error_msg': "K_MEANS_CLUSTERS must be an integer greater than 1"
        }
    }
    
    missing_vars = []
    invalid_vars = []
    
    for var_name, rules in env_rules.items():
        value = os.getenv(var_name)
        required = rules['required']
        
        # Check if variable is required (can be boolean or callable)
        is_required = required() if callable(required) else required
        
        if is_required and not value:
            missing_vars.append(var_name)
            continue
        
        # If value exists and there's a validator, check it
        if value and rules['validator']:
            try:
                if not rules['validator'](value):
                    invalid_vars.append({
                        'name': var_name,
                        'error': rules['error_msg'],
                        'value': value
                    })
            except Exception as e:
                invalid_vars.append({
                    'name': var_name,
                    'error': f"Validation error: {str(e)}",
                    'value': value
                })
    
    if missing_vars:
        raise EnvironmentError(
            error_type=EnvErrorType.MISSING_VARIABLE,
            message="Missing required environment variables",
            details={"missing_variables": missing_vars},
            suggestion="Add the missing variables to your .env file"
        )
    
    if invalid_vars:
        raise EnvironmentError(
            error_type=EnvErrorType.INVALID_VALUE,
            message="Invalid environment variable values",
            details={"invalid_variables": invalid_vars},
            suggestion="Check the format of the specified variables"
        )
    
    logger.info("Environment configuration check completed successfully")

def get_environment_config() -> Dict[str, Any]:
    """
    Get the current environment configuration.
    Returns a dictionary with all environment settings.
    """
    config = {
        'debug_mode': os.getenv('DEBUG', 'true').lower() == 'true',
        'qdrant_url': os.getenv('QDRANT_URL'),
        'qdrant_api_key': os.getenv('QDRANT_API_KEY'),
        'memory_limit_gb': _parse_memory_limit('MEMORY_LIMIT_GB'),
        'gpu_memory_limit': _parse_memory_limit('GPU_MEMORY_LIMIT'),
        'log_level': os.getenv('LOG_LEVEL', 'INFO').upper()
    }
    
    return config

def _parse_memory_limit(env_var: str) -> Optional[int]:
    """Parse memory limit from environment variable"""
    value = os.getenv(env_var)
    if value:
        try:
            limit = int(value)
            return limit if limit > 0 else None
        except ValueError:
            logger.warning(f"Invalid {env_var} value: {value}")
    return None 