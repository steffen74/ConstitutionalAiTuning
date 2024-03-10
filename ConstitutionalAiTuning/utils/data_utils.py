import csv
from typing import List, Dict, Optional

def import_prompts_from_csv(csv_file: str, prompt_column: str = 'prompt', id_column: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Import prompts from a CSV file.

    Args:
        csv_file (str): Path to the CSV file.
        prompt_column (str, optional): Name of the column containing the prompts. Defaults to 'prompt'.
        id_column (str, optional): Name of the column containing the IDs. If None, the row number is used as the ID. Defaults to None.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, where each dictionary contains an 'id' key and a 'prompt' key.
    """
    prompts = []

    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)

        for i, row in enumerate(reader, start=1):
            prompt_text = row[prompt_column]
            prompt_id = row[id_column] if id_column else str(i)
            prompts.append({'id': prompt_id, 'prompt': prompt_text})

    return prompts