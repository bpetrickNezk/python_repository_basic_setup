"""Write tests for every function you write."""

import json
import tempfile
from pathlib import Path

import pandas as pd
import pytest
from pandera.typing import DataFrame
from pydantic import ValidationError

from functions.example_function import UserProfile, UserSchema, calculate_bmi, normalize_user_names


def test_normalize_user_names() -> None:
    # Arrange: raw user data with inconsistent names
    raw_data = pd.DataFrame({"user_id": [1, 2, 3], "name": ["  alice", "BOB  ", "  Charlie  "]})

    # Act: normalize the names
    result: DataFrame[UserSchema] = normalize_user_names(raw_data)

    # Assert: values are cleaned as expected
    expected_names = ["Alice", "Bob", "Charlie"]
    assert result["name"].tolist() == expected_names

    # assert schema is still valid
    UserSchema.validate(result)


def test_user_profile_serialization_io():
    """NOTE: a Pydantic class can simply be dumped into json and loaded back."""
    user = UserProfile(user_id=1, name="Alice", height_cm=170, weight_kg=60)

    # Serialize to JSON string
    json_data = user.model_dump_json(indent=3)

    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = Path(tmp_dir) / "user.json"

        # Write to file
        with open(file_path, "w") as f:
            f.write(json_data)

        # Read back into a Python dict
        with open(file_path, "r") as f:
            data = json.load(f)

    # Deserialize from JSON string
    loaded_user = UserProfile.model_validate(data)

    # Assert original and loaded are equal
    assert loaded_user == user


def test_calculate_bmi():
    user = UserProfile(user_id=1, name="Bob", height_cm=180, weight_kg=75)
    bmi = calculate_bmi(user)

    assert bmi == 23.15  # 75 / (1.8^2) = 23.148... → 23.15


def test_user_profile_negative_weight():
    with pytest.raises(ValidationError) as exc_info:
        UserProfile(user_id=2, name="Bob", height_cm=180, weight_kg=-65)

    errors = exc_info.value.errors()
    assert any(err["loc"] == ("weight_kg",) and "greater than 0" in err["msg"] for err in errors)


def test_user_profile_empty_name():
    # test that an empty name is not allowed, the test does not need to be fancy, just make it fail
    with pytest.raises(ValidationError):
        UserProfile(user_id=3, name="", height_cm=180, weight_kg=70)
