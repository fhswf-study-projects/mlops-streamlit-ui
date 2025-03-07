import os
import sys
import logging

import streamlit as st
import streamlit_authenticator as stauth

from app.reloader import reload_ui
from app.constants import EnvConfig


logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Get Your Prediction",
    layout="centered",
)

authenticator = stauth.Authenticate(os.environ.get(EnvConfig.AUTH_CONFIG_FILE.value))  # type: ignore


if __name__ == "__main__":
    try:
        # --- AUTH ---
        authenticator.login(
            fields={
                "Form name": "Sign in",
                "Username": "Username",
                "Password": "Password",
                "Login": "Log in",
            }
        )

        if st.session_state["authentication_status"] is False:
            st.error("Username/password is incorrect")

        if st.session_state["authentication_status"]:
            st.write(f"Welcome *{st.session_state['name']}*")

            reload_ui()
            logger.info("Streamlit app started!")

    except KeyboardInterrupt:
        logger.info("Shutting Down: Process interrupeted")
    except Exception:
        logger.exception("Shutting Down: Exception in main process")
        sys.exit(0)
