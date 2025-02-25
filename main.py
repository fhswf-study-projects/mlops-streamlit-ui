import os
import sys
import logging

import streamlit as st
import streamlit_authenticator as stauth
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.logs import LogEmitterProvider
from opentelemetry.exporter.otlp.proto.grpc.logs_exporter import OTLPLogExporter
from opentelemetry.sdk.logs.export import BatchLogRecordProcessor

from app.constants import EnvConfig


# Set up OpenTelemetry logging
log_provider = LogEmitterProvider()
log_exporter = OTLPLogExporter(endpoint=os.environ.get(EnvConfig.OTEL_EXPORTER_OTLP_ENDPOINT.value), insecure=True)
log_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

# Apply logging instrumentation
LoggingInstrumentor().instrument(set_logging_format=True)

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, os.environ.get(EnvConfig.OTEL_LOG_LEVEL.value)))

st.set_page_config(
    page_title="Get Your Prediction",
    layout="centered",
)

authenticator = stauth.Authenticate(os.environ.get(EnvConfig.AUTH_CONFIG_FILE.value))


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

            from app.ui import main

            main()
            logger.info("Streamlit app started!")

    except KeyboardInterrupt:
        logger.info("Shutting Down: Process interrupeted")
    except Exception:
        logger.exception("Shutting Down: Exception in main process")
        sys.exit(0)
