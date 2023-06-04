"""
Handles the configuration and secrets.
"""
from pathlib import Path
import toml


PROJECT_DIR = Path(__file__).parent.parent.parent

secrets_path = PROJECT_DIR / "secrets.toml"


if not secrets_path.exists():
    print(list(PROJECT_DIR.glob("*")))
    raise FileNotFoundError(f"No secrets.toml file found in {PROJECT_DIR}")


SECRETS = toml.load(secrets_path)
