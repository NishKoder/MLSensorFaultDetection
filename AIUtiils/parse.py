from typing import List


def parse_requirements(filepath: str) -> List[str]:
    """Parses a requirements file into a list of dependencies.

    Args:
        filepath: Path to the requirements file.

    Returns:
        A list of dependencies.
    """
    with open(filepath, 'r', encoding="utf-8") as file:
        return [
            line.strip()
            for line in file
            if line.strip() and not line.startswith('#')
        ]