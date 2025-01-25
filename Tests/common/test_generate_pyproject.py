import toml
from unittest.mock import mock_open, patch

from utils.parse import parse_requirements
from generate_pyproject import (
    update_dependencies,
    update_optional_dependencies,
    write_toml_file,
    main,
)


def test_parse_requirements_valid_file() -> None:
    """Test parsing a valid requirements file."""
    requirements_content = (
        "requests>=2.28.0\n"
        "numpy==1.23.0\n"
        "# This is a comment\n"
        "pandas~=1.5.0\n"
    )
    with patch(
        "builtins.open", mock_open(read_data=requirements_content)
    ) as mock_file:
        dependencies = parse_requirements("requirements.txt")
        mock_file.assert_called_once_with(
            "requirements.txt", 'r', encoding="utf-8"
        )
        assert dependencies == [
            "requests>=2.28.0",
            "numpy==1.23.0",
            "pandas~=1.5.0",
        ]


def test_parse_requirements_empty_file() -> None:
    """Test parsing an empty requirements file."""
    with patch("builtins.open", mock_open(read_data="")) as mock_file:
        dependencies = parse_requirements("empty.txt")
        mock_file.assert_called_once_with(
            "empty.txt", 'r', encoding="utf-8"
        )
        assert dependencies == []


def test_parse_requirements_with_comments() -> None:
    """Test parsing a requirements file with comments and blank lines."""
    requirements_content = "# Comment\n\nrequests==2.28.0\n"
    with patch(
        "builtins.open",
        mock_open(read_data=requirements_content)
    ) as mock_file:
        dependencies = parse_requirements("requirements.txt")
        mock_file.assert_called_once_with(
            "requirements.txt", 'r', encoding="utf-8"
        )
        assert dependencies == ["requests==2.28.0"]


def test_update_dependencies() -> None:
    """Test updating dependencies in the TOML config."""
    config = {"project": {"dependencies": []}}
    dependencies = ["requests>=2.28.0", "numpy==1.23.0"]
    update_dependencies(config, dependencies)
    assert config["project"]["dependencies"] == dependencies


def test_update_optional_dependencies() -> None:
    """Test updating optional dependencies in the TOML config."""
    config = {"project": {"optional-dependencies": {"dev": []}}}
    dev_dependencies = ["pytest>=7.0", "flake8"]
    update_optional_dependencies(config, dev_dependencies)
    assert config["project"]["optional-dependencies"]["dev"] == dev_dependencies


def test_write_toml_file(tmp_path) -> None:
    """Test writing the TOML config to a file."""
    config = {"project": {"name": "my-project", "version": "0.1.0"}}
    filepath = tmp_path / "pyproject.toml"
    write_toml_file(str(filepath), config)
    with open(filepath, "r") as f:
        content = toml.load(f)
    assert content == config


@patch("generate_pyproject.parse_requirements")
@patch("generate_pyproject.update_dependencies")
@patch("generate_pyproject.update_optional_dependencies")
@patch("generate_pyproject.write_toml_file")
@patch("builtins.open", new_callable=mock_open, read_data="[project]\nname = \"test\"")
def test_main_functionality(
    mock_file,
    mock_write_toml,
    mock_update_optional_deps,
    mock_update_deps,
    mock_parse_reqs
):
    """Test the main function's behavior."""
    mock_parse_reqs.side_effect = [["dep1"], ["dev-dep1"]]
    main()

    assert mock_parse_reqs.call_count == 2
    mock_parse_reqs.assert_any_call('requirements.txt')
    mock_parse_reqs.assert_any_call('requirements-dev.txt')
    
    assert mock_update_deps.call_count == 1
    assert mock_update_optional_deps.call_count == 1
    mock_write_toml.assert_called_once()