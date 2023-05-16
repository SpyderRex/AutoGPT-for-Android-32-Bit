import os
from unittest.mock import Mock, patch

import pytest
import requests
from colorama import Fore
from git import Repo

from autogpt.utils import (
    clean_input,
    readable_file_size,
    validate_yaml_file,
)
from tests.utils import skip_in_ci


def test_validate_yaml_file_valid():
    with open("valid_test_file.yaml", "w") as f:
        f.write("setting: value")
    result, message = validate_yaml_file("valid_test_file.yaml")
    os.remove("valid_test_file.yaml")

    assert result == True
    assert "Successfully validated" in message


def test_validate_yaml_file_not_found():
    result, message = validate_yaml_file("non_existent_file.yaml")

    assert result == False
    assert "wasn't found" in message


def test_validate_yaml_file_invalid():
    with open("invalid_test_file.yaml", "w") as f:
        f.write(
            "settings:\n  first_setting: value\n  second_setting: value\n    nested_setting: value\n  third_setting: value\nunindented_setting: value"
        )
    result, message = validate_yaml_file("invalid_test_file.yaml")
    os.remove("invalid_test_file.yaml")
    print(result)
    print(message)
    assert result == False
    assert "There was an issue while trying to read" in message


def test_readable_file_size():
    size_in_bytes = 1024 * 1024 * 3.5  # 3.5 MB
    readable_size = readable_file_size(size_in_bytes)

    assert readable_size == "3.50 MB"



if __name__ == "__main__":
    pytest.main()
