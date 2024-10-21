import threading
import time
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play
import tkinter as tk
from tkinter import scrolledtext

class ComfyAnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = ComfyAnyType("*")

class BWIZ_ErrorDetector:
    def __init__(self):
        self.sound_directory = Path(__file__).parent / "res" / "navi"
        self.log_file_path = Path(__file__).parent / "logs" / "comfyui_log.txt"
        self.error_keyword = "ERROR"    
        
        # Debug prints to check paths
        print(f"Sound directory path: {self.sound_directory}")
        print(f"Log file path: {self.log_file_path}")
        
        self.ensure_log_file_exists()
        self.init_gui()

    def ensure_log_file_exists(self):
        try:
            # Ensure the logs directory exists
            self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
            print(f"Log directory exists: {self.log_file_path.parent.exists()}")

            # Create the log file if it doesn't exist
            if not self.log_file_path.exists():
                self.log_file_path.touch()
                print("Log file created.")
            else:
                print("Log file already exists.")
        except Exception as e:
            print(f"Failed to ensure log file exists: {str(e)}")

    def init_gui(self):

        self.root = tk.Tk()
        self.root.title("Log Monitor")
        self.textbox = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=30)
        self.textbox.pack(padx=10, pady=10)
        self.update_log_content()
        self.root.mainloop()

    def update_log_content(self):
        try:
            with open(self.log_file_path, 'r') as log_file:
                log_content = log_file.read()
                self.textbox.delete(1.0, tk.END)
                self.textbox.insert(tk.END, log_content)
                if self.detect_error(log_content, self.error_keyword):
                    self.play_error_sound()
        except Exception as e:
            print(f"Error reading log file: {str(e)}")
        self.root.after(5000, self.update_log_content)

    def detect_error(self, input, error_keyword):
        if isinstance(input, str):
            return error_keyword.upper() in input.upper()
        return False

    def play_error_sound(self):
        error_sound_file = self.sound_directory / "error.mp3"
        print(f"Attempting to play error sound from: {error_sound_file}")

        # Check if the error sound file exists
        print(f"Error sound file exists: {error_sound_file.exists()}")

        if error_sound_file.exists():
            try:
                sound = AudioSegment.from_file(error_sound_file)
                play(sound)
                print("Error sound played successfully.")
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
    CATEGORY = "BWIZ Nodes/Error Handling"

if __name__ == "__main__":
    error_detector = BWIZ_ErrorDetector()
