import streamlit as st
import pandas as pd
from get_features import get_features

features = get_features()
user_inputs = {}

with st.form("user_input_form"):
    for feature, params in features.items():
        if params["type"] == "number":
            converted_name = feature.capitalize().replace("_", " ")
            user_inputs[converted_name] = st.number_input(
                converted_name,
                min_value=params["min_value"],
                max_value=params["max_value"],
                help=params["help"],
                key=converted_name,,
            )
        elif params["type"] == "select":
            converted_name = feature.capitalize().replace("_", " ")
            user_inputs[converted_name] = st.selectbox(
                converted_name,
                options=params["options"],
                help=params["help"],
                key=converted_name,
            )

    submitted = st.form_submit_button("Submit")
    if submitted:
        prediction = None
        st.subheader("Your Submitted Data")

        data = (
            pd.DataFrame([user_inputs]).T.rename(columns={0: "Your Inputs"}).astype(str)
        )
        data.index.names = ["Categories"]
        st.dataframe(data, use_container_width=True, key="user_inputs")

        st.write("Predicted Income:", f"**{prediction}**")
