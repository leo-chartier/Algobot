import json
import os
from typing import Any

DIR_PATH = "../config"
EMPTY_TEMPLATES = {
    "bot": {"token": ""}
}



def load(name: str = "bot") -> Any:
    path = os.path.join(os.path.dirname(__file__), DIR_PATH, name + ".json")

    if not os.path.isfile(path):
        if name not in EMPTY_TEMPLATES:
            raise FileNotFoundError(f"Missing '{name}' configuration file")
        
        os.makedirs(os.path.dirname(path), exist_ok=True)

        save(name, EMPTY_TEMPLATES[name])
        raise FileNotFoundError(f"Missing '{name}' configuration file. An empty one has been created for you.")

    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # if not isinstance(config, dict):
    #     raise ValueError("Configuration must be a dictionary.")
    
    return config

def save(name: str, data: Any) -> None:
    path = os.path.join(os.path.dirname(__file__), DIR_PATH, name + ".json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)