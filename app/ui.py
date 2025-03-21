import time
import logging

import streamlit as st
import pandas as pd

from app.schemas import get_features
from app.backend import get_prediction, send_data_for_predition
from opentelemetry.metrics import get_meter

MAX_WAIT_TIME = 120  # in seconds

logger = logging.getLogger(__name__)

meter = get_meter("metric_for_mlflow")

counter_feedback = meter.create_counter(
    name="counter_user_feedback", description="Feedback of a user if the prediction was correct or not", unit="1",
)

features = get_features()

if "user_input" not in st.session_state:
    st.session_state["user_inputs"] = {}

st.title("🔮 AI Prediction System")
st.write("Enter your data below to get a prediction.")

with st.form("user_input_form"):
    for feature, params in features.items():
        if params["type"] == "number":
            converted_name = feature.capitalize().replace("_", " ")
            st.session_state["user_inputs"][converted_name] = st.number_input(
                converted_name,
                min_value=params["min_value"],
                max_value=params["max_value"],
                help=params["help"],
                key=converted_name,
            )
        elif params["type"] == "select":
            converted_name = feature.capitalize().replace("_", " ")
            st.session_state["user_inputs"][converted_name] = st.selectbox(
                converted_name,
                options=params["options"],
                help=params["help"],
                key=converted_name,
            )

    submitted = st.form_submit_button("Submit")

result = None
if submitted:
    st.subheader("Your Submitted Data")

    data = (
        pd.DataFrame([st.session_state["user_inputs"]])
        .T.rename(columns={0: "Your Inputs"})
        .astype(str)  # type: ignore
    )
    data.index.names = ["Categories"]
    st.dataframe(data, use_container_width=True, key="user_inputs")

    user_inputs_api = {
        k.lower().replace(" ", "_"): v
        for k, v in st.session_state["user_inputs"].items()
    }
    task_id = send_data_for_predition(user_inputs_api)
    logger.info(f"Awaiting result of task: {task_id}")

    st.subheader("Your Prediction")
    if task_id:
        st.write(f"Task started! Task ID: {task_id}")

        start_time = time.time()
        result_placeholder = st.empty()

        # with st.spinner("Processing... Please wait."):
        while time.time() - start_time < MAX_WAIT_TIME:
            result = get_prediction(task_id)
            if result is not None:
                logger.info(
                    f"Prediction took: {time.time() - start_time} seconds to process"
                )
                result_placeholder.write(f"**{result}**")
                break

            time.sleep(3)  # Poll every 3 seconds
        else:
            logging.warning("Task timed out after 2 minutes.")
    else:
        logging.warning("Failed to start task.")

st.divider()
st.title("Feedback")
st.write("Was this prediction Correct?")

col1, col2 = st.columns(2)

with col1:
    if st.button("👍 Correct Prediction"):
        st.success("Thank you for your feedback!")
        counter_feedback.add(1, attributes={"Feedback_Pos": "Positive"})
        logging.info("Received feedback!")

with col2:
    if st.button("👎 False Prediction"):
        counter_feedback.add(1, attributes={"Feedback_Neg": "Negative"})
        st.success("Thank you for your feedback!")
        logging.info("Received feedback!")
