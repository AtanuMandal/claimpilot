from pydantic import ValidationError
__version__ = "0.1.0"



def main() -> None:
    from claimpilot.config import get_settings

    try:
        settings = get_settings()
    except ValidationError as err:
        missing = ", ".join(str(e["loc"][0]).upper() for e in err.errors())
        raise SystemExit(
            f"Configuration error: {missing} is missing or invalid.\n"
            "Copy .env.example to .env and fill in the values."
        ) from None

    print(f"ClaimPilot {__version__} is ready.")
    print(f"  environment : {settings.app_env}")
    print(f"  model       : {settings.llm_model}")
    print(f"  API key     : {settings.google_api_key}")  # SecretStr prints as **********