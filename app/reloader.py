"""Workaround force reloading changes on the streamlit page,
since we separated authentication and ui.
Force reloading via importlib is needed since import in Python does lazy-loading.
"""

import importlib


RELOAD_COUNTER = 0


def reload_ui():
    global RELOAD_COUNTER

    from app import ui

    if RELOAD_COUNTER != 0:
        importlib.reload(ui)

    RELOAD_COUNTER += 1
