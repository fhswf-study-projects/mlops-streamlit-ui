import streamlit as st
import pandas as pd


class UserInput:
    def __init__(self, features):
        """
        Dynamically initializes attributes and UI elements based on feature types.
        """
        self.features = features
        self.prediction = None  # Default prediction attribute
        self.user_inputs = {}  # Store user inputs

    def get_inputs(self):
        """Dynamically generates input fields based on the feature dictionary."""
        with st.form("user_input_form"):
            for feature, params in self.features.items():
                if params["type"] == "number":
                    converted_name = feature.capitalize().replace("_", " ")
                    self.user_inputs[converted_name] = st.number_input(
                        converted_name,
                        min_value=params["min_value"],
                        max_value=params["max_value"],
                        value=params["value"],
                        help=params["help"]
                    )
                elif params["type"] == "select":
                    converted_name = feature.capitalize().replace("_", " ")
                    self.user_inputs[converted_name] = st.selectbox(
                        converted_name,
                        options=params["options"],
                        index=params["index"],
                        help=params["help"]
                    )

            submitted = st.form_submit_button("Submit")
            if submitted:
                self.show_results()

    def show_results(self):
        """Display submitted values."""
        st.subheader("Your Submitted Data")

        data = pd.DataFrame([self.user_inputs]).T.rename(columns={0: "Your-Inputs"})
        data.index.names = ["Categories"]
        st.dataframe(data, use_container_width=True)

        st.write(f"Predicted Income:", f"**{self.prediction}**")

user_input = UserInput(
    {
            "age": {"type": "number", "min_value": 0, "max_value": 200, "value": 10, "help": "Insert your age."},
            "workclass": {"type": "select", "options": ["Private", "Local-gov"], "index": 0, "help": "Select your workclass."},
            "fnlwgt": {"type": "number", "min_value": 1, "max_value": 10000000, "value": 10, "help": "Insert your fnlwgt."},
            "education": {"type": "select", "options": ["HS-grad", "Some-college"], "index": 0, "help": "Select your education."},
            "educational_num": {"type": "number", "min_value": 1, "max_value": 16, "value": 10, "help": "Insert your educational-num."},
            "marital_status": {"type": "select", "options": ["Married-civ-spouse", "Divorced"], "index": 0, "help": "Select your marital status."},
            "occupation": {"type": "select", "options": ["Exec-managerial", "Craft-repair"], "index": 0, "help": "Select your occupation."},
            "relationship": {"type": "select", "options": ["Husband", "Wife"], "index": 0, "help": "Select your relationship."},
            "race": {"type": "select", "options": ["Black", "White"], "index": 0, "help": "Select your race."},
            "gender": {"type": "select", "options": ["Male", "Female"], "index": 0, "help": "Select your gender."},
    }
)
user_input.get_inputs()