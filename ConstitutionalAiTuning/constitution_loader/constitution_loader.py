import json

def load_constitution(file_path):
    """
    Loads a constitution file (JSON format) and returns the parsed content.

    :param file_path: The path to the JSON file containing the constitution.
    :return: A dictionary representing the loaded constitution.
    """
    try:
        with open(file_path, 'r') as f:
            constitution = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Constitution file not found at: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")

    return constitution
