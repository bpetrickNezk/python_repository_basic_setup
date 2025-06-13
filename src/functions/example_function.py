"""A Collection of functions

Author: Your Name
Date: 2025

NOTE: use type hints like pandera to define what you are expecting in your function.
      Especially DataFrames will become hard to read if the code base becomes large and
      no one understands which input is expected.
NOTE: use Pydantic to create data classes
"""

import pandera.pandas as pa
from pydantic import BaseModel, Field


# Define the pandera schema as a class
class UserSchema(pa.DataFrameModel):
    """A pandera schema class, to be used as a type hint for a function input"""

    user_id: pa.typing.Series[int] = pa.Field(nullable=False)
    """Describe the kind of user_id that is expected here."""

    name: pa.typing.Series[str] = pa.Field(nullable=False)
    """Describe the kind of name that is expected here."""


def normalize_user_names(df: UserSchema) -> UserSchema:
    """Validates and normalizes user names in a DataFrame using a Pandera schema.

    The normalization:
    - Strips leading/trailing whitespace
    - Capitalizes the first character of the name

    Args:
        df (UserSchema): A DataFrame containing 'user_id' and 'name' columns.

    Returns:
        UserSchema: A new DataFrame with normalized 'name' values.

    Raises:
        pandera.errors.SchemaError: If the DataFrame does not match the expected schema.
    """
    validated_df = UserSchema.validate(df)

    # Normalize names
    validated_df["name"] = validated_df["name"].str.strip().str.capitalize()

    return validated_df


class UserProfile(BaseModel):
    """Work with pydantic to easy serialize your data."""

    user_id: int
    """Describe the expected user id."""

    name: str = Field(min_length=1)
    """Describe the expected name."""

    height_cm: float = Field(gt=0)
    """The hight for the user_id."""

    weight_kg: float = Field(gt=0)
    """The weight for the user_id."""


def calculate_bmi(user: UserProfile) -> float:
    """Calculates the BMI (Body Mass Index) of a user.

    BMI = weight (kg) / (height (m))^2

    Args:
        user (UserProfile): The user's profile with height and weight.

    Returns:
        float: The calculated BMI rounded to 2 decimal places.
    """
    height_m = user.height_cm / 100
    bmi = user.weight_kg / (height_m**2)
    return round(bmi, 2)
