import pytest
from PySide6.QtWidgets import QApplication
from app_v1.gui import TTSApp


@pytest.fixture
def app_instance(qtbot):
    """Fixture to create and return a TTSApp instance."""
    app = TTSApp()
    qtbot.addWidget(app)
    return app


def test_ttsapp_initialization(app_instance):
    """Test that TTSApp initializes correctly."""
    assert isinstance(app_instance, TTSApp), "TTSApp instance should be created."
    assert hasattr(app_instance, "input_button"), "Missing input_button."
    assert hasattr(app_instance, "output_button"), "Missing output_button."
    assert hasattr(app_instance, "run_button"), "Missing run_button."
    assert hasattr(app_instance, "progress_bar"), "Missing progress_bar."