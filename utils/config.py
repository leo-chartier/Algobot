import json
import os
from typing import Any

DIR_PATH = "../config"
EMPTY_TEMPLATES = {
    "bot": {"token": ""}
}



def load(name: str = "bot") -> dict[str, Any]:
    path = os.path.join(os.path.dirname(__file__), DIR_PATH, name + ".json")

    if not os.path.isfile(path):
        if name not in EMPTY_TEMPLATES:
            raise FileNotFoundError(f"Missing '{name}' configuration file")
        
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:
            json.dump(EMPTY_TEMPLATES[name], f, indent=4)
        raise FileNotFoundError(f"Missing '{name}' configuration file. An empty one has been created for you.")

    with open(path, "r") as f:
        config = json.load(f)

    if not isinstance(config, dict):
        raise ValueError("Configuration must be a dictionary.")
    
    return config
