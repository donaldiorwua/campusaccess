import json
from pathlib import Path


def save_requests(cadrs, file_path):
    if not isinstance(cadrs, dict):
        raise TypeError("card must be a dictionary")

    path = Path(file_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(cadrs, file, indent=4)
    except (OSError, TypeError, ValueError) as error:
        raise ValueError(
            f"Cards could not be saved to '{path}': {error}"
        ) from error
    
def load_requests(file_path):

    path = Path(file_path)
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as file:
            cards = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"invalid JSON in '{path}': {error}"
        )from error
    except OSError as error:
        raise ValueError(
            f"could not read cards from {path}: {error}"
        )from error
    
    if not isinstance(cards, dict):
        raise ValueError(
            f"invalid card data in {path}: "
            "expected a JSON object keyed by ticket ID"
        )
    
    return cards