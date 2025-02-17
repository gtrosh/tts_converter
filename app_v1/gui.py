import sys
from pathlib import Path
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog,
    QLabel, QHBoxLayout, QSizePolicy, QProgressBar
)
from PySide6.QtCore import Qt, QTimer
from app_v1.tts_engine import TTSThread


class TTSApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Portuguese TTS Converter")
        
        app_font = QFont("Verdana", 12)
        self.setFont(app_font)

        with open("app_v1/styles.qss", "r") as f:
            self.setStyleSheet(f.read())

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        button_font = QFont("Verdana", 12)

        self.file_label = QLabel("Select files:")
        main_layout.addWidget(self.file_label)

        file_buttons_layout = QHBoxLayout()
        file_buttons_layout.setSpacing(10)

        button_min_width = 190

        self.input_button = QPushButton("Add Text File", self)
        self.input_button.setObjectName("input_button")
        self.input_button.setFont(button_font)
        self.input_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.input_button.setMinimumWidth(button_min_width)
        self.input_button.clicked.connect(self.select_input_file)
        file_buttons_layout.addWidget(self.input_button)

        self.output_button = QPushButton("Select Output Location", self)
        self.output_button.setObjectName("output_button")
        self.output_button.setFont(button_font)
        self.output_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.output_button.setMinimumWidth(button_min_width)
        self.output_button.clicked.connect(self.select_output_file)
        file_buttons_layout.addWidget(self.output_button)

        main_layout.addLayout(file_buttons_layout)

        self.run_button = QPushButton("Convert", self)
        self.run_button.setObjectName("run_button")
        self.run_button.setFont(button_font)
        self.run_button.clicked.connect(self.convert_text_to_speech)
        main_layout.addWidget(self.run_button)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        self.setLayout(main_layout)
        self.adjustSize()

        self.input_file = ""
        self.output_file = ""

    def select_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.input_file = Path(file_path)
            self.file_label.setText(f"Selected: {self.input_file.name}")

            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(False)

    def select_output_file(self):
        default_name = "output.wav"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Select Output File", default_name,
            "Audio Files (*.wav);;All Files (*)"
        )

        if file_path:
            if not file_path.endswith(".wav"):
                file_path += ".wav"
            self.output_file = file_path
            self.file_label.setText(f"Saving as: {Path(file_path).name}")

    def convert_text_to_speech(self):
        if not self.input_file or not self.output_file:
            self.file_label.setText("Error: Select both input and output files!")
            return

        self.file_label.setText("Processing...")
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        self.thread = TTSThread(self.input_file, self.output_file)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished_signal.connect(self.conversion_finished)
        self.thread.start()

    def update_progress(self, value, message=""):
        self.progress_bar.setValue(value)
        if message:
            self.progress_bar.setFormat(message)

    def conversion_finished(self, message):
        self.file_label.setText(message)
        self.progress_bar.setFormat("Done!")
        QTimer.singleShot(1500, self.hide_progress_bar)
    
    def hide_progress_bar(self):
        self.progress_bar.setVisible(False)
