import sys
from PySide6.QtWidgets import QApplication
from app_v1.gui import TTSApp  # Importing the GUI class

def main():
    """ Main entry point of the application. """
    app = QApplication(sys.argv)
    window = TTSApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
