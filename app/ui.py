import time
import logging

import streamlit as st
import pandas as pd

from app.schemas import get_features
from app.backend import get_prediction, send_data_for_predition, send_data_to_with_task_id_to_backend
from opentelemetry.metrics import get_meter

#####################################################################
# Logger, Metrics and Setup
#####################################################################

MAX_WAIT_TIME = 120  # in seconds

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

meter = get_meter("metric_for_mlflow")

counter_feedback = meter.create_counter(
    name="counter_user_feedback", description="Feedback of a user if the prediction was correct or not", unit="1",
)

features = get_features()


def create_input_fields(params: dict, feature: str) -> None:
    """
    Create numeric and categorical input fields for different features.
    """

    if params["type"] == "number":
        with column_numeric:
            converted_name = feature.capitalize().replace("_", " ")
            st.session_state["user_inputs"][converted_name] = st.number_input(
                converted_name,
                min_value=params["min_value"],
                max_value=params["max_value"],
                help=params["help"],
                key=converted_name,
            )
    elif params["type"] == "select":
        with column_categorical:
            converted_name = feature.capitalize().replace("_", " ")
            st.session_state["user_inputs"][converted_name] = st.selectbox(
                converted_name,
                options=params["options"],
                help=params["help"],
                key=converted_name,
            )


def process_prediction(inputs: dict, t_id: str) -> bool:
    """
    Is getting the prediction and returning True if was successful.
    Check MAX_WAIT_TIME seconds (max. user waiting time).
    """
    start_time = time.time()

    while time.time() - start_time < MAX_WAIT_TIME:
        result = get_prediction(t_id)
        if result is not None:
            logger.info(
                f"Prediction took: {time.time() - start_time} seconds to process"
            )
            st.metric("Prediction", result, border=True)
            inputs["income"] = result
            inputs["task_id"] = t_id
            send_data_to_with_task_id_to_backend(user_inputs_api)
            return True

        time.sleep(3)  # Poll every 3 seconds
    else:
        logger.warning("Task timed out after 2 minutes.")
        return False


def show_submitted_data():
    """
    Show submitted data as a table for the user.
    """
    st.subheader("Submitted Data")

    data = (
        pd.DataFrame([st.session_state["user_inputs"]])
        .T.rename(columns={0: "Your Inputs"})
        .astype(str)  # type: ignore
    )
    data.index.names = ["Categories"]
    height = int(35.2*(len(data) + 1))
    st.dataframe(data, use_container_width=True, key="user_inputs", height=height)


def convert_user_inputs_to_a_dict():
    """
    Just converting to a dict, for better API-handling.
    """
    return {
        k.lower().replace(" ", "_"): v
        for k, v in st.session_state["user_inputs"].items()
    }


def send_feedback(attributes):
    counter_feedback.add(1, attributes=attributes)
    logger.info("Received feedback!")
    st.session_state.feedback_response = "Thank you for your feedback!"


#####################################################################
# Predifined states for Streamlit and the app itself
#####################################################################

if "user_input" not in st.session_state:
    st.session_state["user_inputs"] = {}

if "feedback_response" not in st.session_state:
    st.session_state.feedback_response = None

result_received = False

st.title("Income Prediction System")

# The Input User Form
with st.expander("Enter your data below to get a prediction.", expanded=True):
    with st.form("user_input_form", border=False):
        column_numeric, column_categorical = st.columns(2)
        for feature, params in features.items():
            create_input_fields(params, feature)
        submitted = st.form_submit_button("Predict", help="Get prediction", icon=":material/grain:")

# After pressing on Submit this will apear
column_submitted_data, column_results = st.columns(2)
if submitted:
    logger.info("User submitted")
    st.session_state.feedback_response = None
    result = None

    with column_submitted_data:
        show_submitted_data()

    user_inputs_api = convert_user_inputs_to_a_dict()

    task_id = send_data_for_predition(user_inputs_api)
    logger.info(f"Awaiting result of task: {task_id}")

    with column_results:
        st.subheader("Result")
        if task_id is not None:
            with st.expander("Task started! Expand, to show TASK-ID", expanded=False):
                st.write(f"**{task_id}**")
            with st.spinner("Processing... Please wait."):
                result_received = process_prediction(
                    inputs=user_inputs_api,
                    t_id=task_id
                )
        else:
            logger.warning("Failed to start task (no task-id).")

# Feedback-Section
if result_received is True and st.session_state.feedback_response is None:
    st.divider()
    st.title("Feedback")
    st.write("Was this prediction Correct?")

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "Yes, it's correct!",
            icon=":material/thumb_up:",
            help="Click if the prediction is right",
            on_click=send_feedback,
            args=(
                {"Feedback_Pos": "Positive"},
            ),
            use_container_width=True
        )

    with col2:
        st.button(
            "No, it's wrong",
            icon=":material/thumb_down:",
            help="Click if the prediction is incorrect",
            on_click=send_feedback,
            args=(
                {"Feedback_Neg": "Negative"},
            ),
            use_container_width=True
        )

# Feedback for the user, so the user know feedback was successfully
if st.session_state.feedback_response:
    st.success(st.session_state.feedback_response)
    result_received = False
else:
    pass
