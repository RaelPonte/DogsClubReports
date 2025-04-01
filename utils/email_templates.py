from typing import Dict
from pathlib import Path
import re


def load_template(template_name: str) -> str:
    templates_path = Path(__file__).parents[1] / "html"
    file_path = templates_path / f"{template_name}.html"
    with open(file_path, "r") as file:
        return file.read()


def replace_template_variables(template: str, variables: Dict[str, str]) -> str:
    """
    Replace template variables in the given template with values from the given dictionary.

    Args:
        template: The template string
        variables: A dictionary of key-value pairs where the key is the variable name
            and the value is the value to replace

    Returns:
        The template string with the variables replaced
    """
    for key, value in variables.items():
        pattern = r"\{\{" + key + r"\}\}"
        template = re.sub(pattern, value, template)
    return template

