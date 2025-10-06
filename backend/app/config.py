import os
from pathlib import Path

# Load environment variables from .env file if it exists
def load_env_file():
    """Load environment variables from .env file"""
    env_file = Path(__file__).parent.parent.parent / '.env'
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

# Load .env file on module import
load_env_file()

def auth_disabled() -> bool:
    return os.getenv("DISABLE_AUTH", "false").strip().lower() in {"1", "true", "yes"}

def org_name() -> str:
    return os.getenv("ORG_NAME", "Reliance Jio Infotech Solutions")

def get_mongodb_uri() -> str:
    return os.getenv("MONGODB_URI", "")

def get_gemini_api_key() -> str:
    return os.getenv("GOOGLE_GEMINI_API_KEY", "")


