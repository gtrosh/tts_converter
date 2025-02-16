from pathlib import Path
from PySide6.QtCore import QThread, Signal
from TTS.api import TTS


class TTSThread(QThread):
    """ Background thread to run TTS conversion without freezing UI """
    progress = Signal(int)
    finished_signal = Signal(str)

    def __init__(self, input_file, output_file):
        super().__init__()
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)

    def run(self):
        try:
            self.progress.emit(10)  # Start progress

            # Load the Coqui TTS model
            self.progress.emit(30)
            tts = TTS(model_name="tts_models/pt/cv/vits", progress_bar=False, gpu=False)

            # Read text from file
            self.progress.emit(50)
            text = self.input_file.read_text(encoding="utf-8").strip()

            # Convert text to speech
            self.progress.emit(70)
            tts.tts_to_file(text=text, file_path=str(self.output_file))

            self.progress.emit(100)  # Complete
            self.finished_signal.emit(f"Audio saved as: {self.output_file.name}")

        except Exception as e:
            self.finished_signal.emit(f"Error: {str(e)}")
