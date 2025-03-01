from unittest.mock import patch

import pandas as pd
from streamlit.testing.v1 import AppTest


def mock_get_features() -> dict:
    """
    Mocked version of get_features() for consistent testing.
    """
    return {
        "age": {
            "type": "number",
            "min_value": 0,
            "max_value": 200,
            "help": "Insert your age.",
        },
        "workclass": {
            "type": "select",
            "options": ["Private", "Local-gov"],
            "help": "Select your workclass.",
        },
        "fnlwgt": {
            "type": "number",
            "min_value": 1,
            "max_value": 10000000,
            "help": "Insert your fnlwgt.",
        },
        "education": {
            "type": "select",
            "options": ["HS-grad", "Some-college"],
            "help": "Select your education.",
        },
        "educational_num": {
            "type": "number",
            "min_value": 1,
            "max_value": 16,
            "help": "Insert your educational-num.",
        },
        "marital_status": {
            "type": "select",
            "options": ["Married-civ-spouse", "Divorced"],
            "help": "Select your marital status.",
        },
        "occupation": {
            "type": "select",
            "options": ["Exec-managerial", "Craft-repair"],
            "help": "Select your occupation.",
        },
        "relationship": {
            "type": "select",
            "options": ["Husband", "Wife"],
            "help": "Select your relationship.",
        },
        "race": {
            "type": "select",
            "options": ["Black", "White"],
            "help": "Select your race.",
        },
        "gender": {
            "type": "select",
            "options": ["Male", "Female"],
            "help": "Select your gender.",
        },
    }


def test_run_app():
    """
    Testing user input functionality. Will get the mocked data (simulating API call) and check if all
    necessary input-field are created. Insert values within the field and check if it matches the expected
    DataFrame.
    """
    with patch("app.schemas.get_features", side_effect=mock_get_features):
        at = AppTest.from_file("app/ui.py").run()

        # Simulate user input
        at.number_input("Age").set_value(25)
        at.selectbox("Workclass").set_value("Private")
        at.number_input("Fnlwgt").set_value(100000)
        at.selectbox("Education").set_value("Some-college")
        at.number_input("Educational num").set_value(2)
        at.selectbox("Marital status").set_value("Divorced")
        at.selectbox("Occupation").set_value("Craft-repair")
        at.selectbox("Relationship").set_value("Husband")
        at.selectbox("Race").set_value("Black")
        at.selectbox("Gender").set_value("Male")

        # Submit form
        at.button[0].click().run()

        # Expected DataFrame
        expected_df = (
            pd.DataFrame(
                {
                    "Categories": [
                        "Age",
                        "Workclass",
                        "Fnlwgt",
                        "Education",
                        "Educational num",
                        "Marital status",
                        "Occupation",
                        "Relationship",
                        "Race",
                        "Gender",
                    ],
                    "Your Inputs": [
                        25,
                        "Private",
                        100000,
                        "Some-college",
                        2,
                        "Divorced",
                        "Craft-repair",
                        "Husband",
                        "Black",
                        "Male",
                    ],
                }
            )
            .astype(str)
            .set_index("Categories")
        )

        # Get actual dataframe
        actual_df = at.dataframe[0].value

        # Assertions
        assert type(actual_df) is type(expected_df), "UNEXPECTED TYPE"
        assert actual_df.equals(expected_df), "UNEXPECTED DATA"
