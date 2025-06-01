import os
from pathlib import Path
from dotenv import load_dotenv

class EnvironmentError(Exception):
    """Custom exception for environment configuration errors"""
    pass

def check_environment():
    """
    Check if all required environment variables are set.
    Raises EnvironmentError if any required variables are missing.
    """
    # Load environment variables from .env file
    env_path = Path(__file__).parent.parent / '.env'
    if not env_path.exists():
        raise EnvironmentError(
            "Missing .env file in backend directory. "
            "Please create one based on .env.example"
        )
    
    load_dotenv(dotenv_path=env_path)
    
    # List of required environment variables
    required_vars = [
        ('DEBUG', 'Boolean flag for debug mode'),
        ('QDRANT_URL', 'URL for the Qdrant vector database'),
        ('QDRANT_API_KEY', 'API key for Qdrant (optional in debug mode)')
    ]
    
    missing_vars = []
    
    for var, description in required_vars:
        value = os.getenv(var)
        
        # Special handling for DEBUG
        if var == 'DEBUG':
            if value is None:
                missing_vars.append(f"{var}: {description}")
            continue
            
        # Special handling for QDRANT_API_KEY (only required in production)
        if var == 'QDRANT_API_KEY' and os.getenv('DEBUG', 'True').lower() == 'true':
            continue
            
        # Check if variable exists and is not empty
        if not value:
            missing_vars.append(f"{var}: {description}")
    
    if missing_vars:
        raise EnvironmentError(
            "Missing required environment variables:\n" + 
            "\n".join(f"- {var}" for var in missing_vars)
        ) 