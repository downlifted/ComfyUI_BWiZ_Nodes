import threading
import time
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")
class BWIZ_ErrorDetector:
    def __init__(self):
        self.sound_directory = Path(__file__).parent / "res" / "navi"
        self.log_file_path = Path(__file__).parent / "logs" / "comfyui_log.txt"
        self.error_keyword = "ERROR"
        
        print(f"Sound directory path: {self.sound_directory}")
        print(f"Log file path: {self.log_file_path}")
        
        self.ensure_log_file_exists()
        self.monitor_log_file()

    def ensure_log_file_exists(self):
        try:
            self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.log_file_path.exists():
                self.log_file_path.touch()
        except Exception as e:
            print(f"Failed to ensure log file exists: {str(e)}")

    def monitor_log_file(self):
        while True:
            try:
                with open(self.log_file_path, 'r') as log_file:
                    log_content = log_file.read()
                    if self.detect_error(log_content, self.error_keyword):
                        self.play_error_sound()
            except Exception as e:
                print(f"Error reading log file: {str(e)}")
            time.sleep(5)  # Check every 5 seconds

    def detect_error(self, input, error_keyword):
        if isinstance(input, str):
            return error_keyword.upper() in input.upper()
        return False

    def play_error_sound(self):
        error_sound_file = self.sound_directory / "error.mp3"
        if error_sound_file.exists():
            try:
                sound = AudioSegment.from_file(error_sound_file)
                play(sound)
            except Exception as e:
                print(f"Failed to play error sound: {str(e)}")
        else:
            print("Error sound file not found.")

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "input": (any, {}),
            "error_keyword": ("STRING", {"default": "ERROR", "multiline": False}),
        }}

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("error_detected",)
    FUNCTION = "detect_error"
    CATEGORY = "BWIZ/Error Handling"

if __name__ == "__main__":
    error_detector = BWIZ_ErrorDetector()
