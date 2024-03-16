import json

def load_principles(file_path):
    """
    Loads a constitutioal principles file (JSON format) and returns the parsed content.

    :param file_path: The path to the JSON file containing the principles.
    :return: A dictionary representing the loaded principles.
    """
    try:
        with open(file_path, 'r') as f:
            principles = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Principles file not found at: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")

    return principles
