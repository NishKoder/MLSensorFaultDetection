from typing import NoReturn
import toml


from utils.types import SimpleJson
from utils.parse import parse_requirements


def update_dependencies(
    config: SimpleJson,
    dependencies: list[str],
) -> None:
    """Updates the dependencies in the TOML configuration.

    Args:
        config: The TOML configuration dictionary.
        dependencies: List of dependencies to update.
    """
    config['project']['dependencies'] = dependencies


def update_optional_dependencies(
    config: SimpleJson,
    dev_dependencies: list[str],
) -> None:
    """Updates the optional dev dependencies in the TOML config.

    Args:
        config: The TOML configuration dictionary.
        dev_dependencies: List of dev dependencies to update.
    """
    config['project']['optional-dependencies']['dev'] = dev_dependencies


def write_toml_file(filepath: str, config: SimpleJson) -> None:
    """Writes the TOML configuration to a file.

    Args:
        filepath: Path to the output file.
        config: The TOML configuration dictionary.
    """
    with open(filepath, 'w', encoding="utf-8") as file:
        toml.dump(config, file)


def main() -> NoReturn:
    """Generates pyproject.toml from template and requirements files."""
    dependencies: list[str] = parse_requirements('requirements.txt')
    dev_dependencies: list[str] = parse_requirements(
        'requirements-dev.txt'
    )

    with open('pyproject.toml.template', 'r', encoding="utf-8") as file:
        config: SimpleJson = toml.load(file)

    update_dependencies(config, dependencies)
    update_optional_dependencies(config, dev_dependencies)

    write_toml_file('pyproject.toml', config)


if __name__ == "__main__":
    main()
