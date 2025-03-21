import os
import logging
from typing import Dict, Union

import requests

from app.constants import EnvConfig


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

API_URL = os.getenv(EnvConfig.API_BASE_URL.value, "http://localhost")

def send_data_to_with_task_id_to_backend(data: Dict) -> Union[str, None]:
    """Send a request to start the task and return the task ID."""
    logger.info("Sending data back with task-id and prediction")
    with requests.Session() as session:
        response = session.post(
            f"{API_URL}/models/predict", # TODO
            headers={
                "Authorization": f"Bearer {os.environ[EnvConfig.API_TOKEN.value]}",
            },
            json=data,
        )
    if response.status_code == 200:
        logger.info("SUCCESS: Sending data back with task-id and prediction")
    return None


def send_data_for_predition(data: Dict) -> Union[str, None]:
    """Send a request to start the task and return the task ID."""
    logger.info("Sending user-inputs to get task-id")
    with requests.Session() as session:
        response = session.post(
            f"{API_URL}/models/predict",
            headers={
                "Authorization": f"Bearer {os.environ[EnvConfig.API_TOKEN.value]}",
            },
            json=data,
        )

    if response.status_code == 200:
        logger.info("SUCCESS: Sending user-inputs to get task-id")
        return response.json().get("id")
    return None


def get_prediction(task_id) -> Union[str, None]:
    """Check the status of the task."""
    logger.info("Sending user-inputs to get prediction")
    with requests.Session() as session:
        response = session.get(
            f"{API_URL}/tasks/check/{task_id}",
            headers={
                "Authorization": f"Bearer {os.environ[EnvConfig.API_TOKEN.value]}",
            },
        )

    if response.status_code == 200:
        r = response.json()
        logger.info("SUCCESS: Sending user-inputs to get prediction")
        return r["result"]["meaning"] if r["status"] != "PENDING" else None
    return None
