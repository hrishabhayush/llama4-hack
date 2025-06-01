import os
from pathlib import Path
from dotenv import load_dotenv
from enum import Enum
from typing import Optional, Dict, Any
from db_log import setup_logger

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
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the error to a dictionary format"""
        return {
            "error_type": self.error_type.value,
            "message": self.message,
            "details": self.details,
            "suggestion": self.suggestion
        }

def check_environment():
    """
    Check if all required environment variables are set.
    Raises EnvironmentError if any required variables are missing.
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
    
    # Required variables and their validation rules
    required_vars = {
        'DEBUG': {
            'required': True,
            'validator': lambda x: x.lower() in ['true', 'false'],
            'error_msg': "DEBUG must be 'True' or 'False'"
        },
        'QDRANT_URL': {
            'required': True,
            'validator': lambda x: x.startswith(('http://', 'https://')),
            'error_msg': "QDRANT_URL must be a valid HTTP/HTTPS URL"
        },
        'QDRANT_API_KEY': {
            'required': lambda: os.getenv('DEBUG', 'True').lower() != 'true',
            'validator': lambda x: bool(x and len(x) > 0),
            'error_msg': "QDRANT_API_KEY is required in production mode"
        }
    }
    
    missing_vars = []
    invalid_vars = []
    
    for var_name, rules in required_vars.items():
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
                        'error': rules['error_msg']
                    })
            except Exception as e:
                invalid_vars.append({
                    'name': var_name,
                    'error': f"Validation error: {str(e)}"
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