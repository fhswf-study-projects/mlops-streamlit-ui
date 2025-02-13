from streamlit.testing.v1 import AppTest

def test_running_app():
    at = AppTest.from_file("streamlit-app\\form.py").run()
    assert not at.exception