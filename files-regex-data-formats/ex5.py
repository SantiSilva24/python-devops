import json
from pathlib import Path

def update_image_tag(config_path: str | Path, service_name: str, new_tag: str) -> None:
    """
    Reads a JSON config file, updates a service's image tag, and writes it back.
    """
    # Input validation.
    if not isinstance(config_path, (str, Path)):
        raise TypeError(f"Config path {str(config_path)} must be a string or a Path object, recieved {type(config_path).__name__!r}")
    
    # normalise to Path so .is_dir() always works
    config_path = Path(config_path)  

    if not config_path.exists():
        raise FileNotFoundError(f"Could not find {config_path}")
    
    if not isinstance(service_name, str):
        raise TypeError("Service name must be a string")
    if not service_name.strip():
        raise ValueError("Service name must be non-empty")
    
    if not isinstance(new_tag, str):
        raise TypeError("New tag must be a string")
    if not new_tag.strip():
        raise ValueError("New tag must be non-empty")
    
    # Open JSON file for reading first
    with config_path.open("r", encoding="utf-8") as file:
        config_data = json.load(file)

    if service_name not in config_data["services"]:
        raise KeyError(f"Service {service_name} not found in file {config_path}")
    
    config_data["services"][service_name]["image_tag"] = new_tag

    # Open JSON for writing now
    with config_path.open("w", encoding="utf-8") as file:
        json.dump(config_data, file, indent=4, sort_keys=True)


config_file = Path("config_ex5.json")
update_image_tag(config_file, "api-gateway", "1.2.1")
    