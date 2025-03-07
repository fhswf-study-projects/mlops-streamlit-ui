import os
from typing import Dict, Union
import logging

import requests

from app.constants import EnvConfig


logger = logging.getLogger(__name__)

API_URL = os.environ[EnvConfig.API_BASE_URL.value]


def send_data_for_predition(data: Dict) -> Union[str, None]:
    """Send a request to start the task and return the task ID."""
    response = requests.post(f"{API_URL}/models/predict", json=data)
    if response.status_code == 200:
        return response.json().get("id")
    return None


def get_prediction(task_id) -> Union[str, None]:
    """Check the status of the task."""
    logger.warning(task_id)
    response = requests.get(f"{API_URL}/tasks/check/{task_id}")
    logger.warning(response)
    if response.status_code == 200:
        r = response.json()
        return r["result"]["meaning"] if r["status"] != "PENDING" else None
    return None
