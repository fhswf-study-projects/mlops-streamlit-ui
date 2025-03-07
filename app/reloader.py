import importlib


RELOAD_COUNTER = 0


def reload_ui():
    global RELOAD_COUNTER

    from app import ui

    if RELOAD_COUNTER != 0:
        importlib.reload(ui)

    RELOAD_COUNTER += 1
