import threading
import time
import os
import random
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play


class ComfyAnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = ComfyAnyType("*")

class BWIZ_NotificationSound:
    def __init__(self):
        self.sound_directory = Path(__file__).parent / "res" / "navi"
        self.temp_dir = Path(__file__).parent / "temp"
        self.temp_dir.mkdir(exist_ok=True)
        self.log_directory = Path(__file__).parent / "logs"
        self.log_directory.mkdir(exist_ok=True)
        self.log_file_path = self.log_directory / "comfyui_log.txt"
        self.error_count = 0  # Counter for error messages
        self.error_limit = 3  # Limit for error messages

    def BWIZ_NotificationSound(self, sound_file, volume):
        try:
            sound = AudioSegment.from_file(sound_file)
            sound = sound + (volume * 10 - 5)  # Adjust volume
            play(sound)
            print(f"Played sound: {sound_file}")
        except Exception as e:
            print(f"Error playing sound: {str(e)}")
            raise

    def read_log_file(self):
        try:
            with open(self.log_file_path, 'r') as log_file:
                return log_file.read()
        except FileNotFoundError as e:
            if self.error_count < self.error_limit:
                print(f"Error reading log file: {str(e)}")
                self.error_count += 1
            return None

    @classmethod
    def INPUT_TYPES(s):
        default_directory = Path(__file__).parent / "res" / "navi"
        return {"required": {
                    "any": (any, {"label": "Input Sound(s): input dir or file here"}), 
                    "mode": (["always", "on empty queue"], {}),
                    "volume": ("FLOAT", {"min": 0, "max": 1, "step": 0.1, "default": 0.5}),
                    "enable_timer": ("BOOLEAN", {"default": False}),
                    "interval_minutes": ("INT", {"default": 0, "min": 0, "step": 1}),
                    "play_error_sound": ("BOOLEAN", {"default": True}),
                    "sound_directory": ("STRING", {"default": str(default_directory), "multiline": False}),
                }}

    FUNCTION = "BWIZ_NotificationSound"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True, True)
    OUTPUT_NODE = True
    RETURN_TYPES = (any, "STRING")
    CATEGORY = "BWIZ Nodes/Sound"

    def IS_CHANGED(self, **kwargs):
        return float("NaN")
class PlaySound:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "any": (any, {}),
            "mode": (["always", "on empty queue"], {}),
            "volume": ("FLOAT", {"min": 0, "max": 1, "step": 0.1, "default": 0.5}),
            "file": ("STRING", {"default": "notify.mp3"})
        }}

    FUNCTION = "BWIZ_NotificationSound"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)
    OUTPUT_NODE = True
    RETURN_TYPES = (any,)

    CATEGORY = "BWIZ Nodes/Sound"

    def IS_CHANGED(self, **kwargs):
        return float("NaN")

    def PlaySound(self, any, mode, volume, file):
        try:
            self._play_sound(file, volume)
        except Exception as e:
            print(f"Failed to play sound: {str(e)}")
        return {"ui": {"a": []}, "result": (any,)}

        
    def _signal_play_error_sound(self, sound_directory):
        directory = Path(sound_directory)
        error_sound_file = directory / "error.mp3"
        print(f"Attempting to play error sound from: {error_sound_file}")

        if error_sound_file.exists():
            print("Error sound file found. Attempting to play...")
            try:
                sound = AudioSegment.from_file(error_sound_file)
                play(sound)
                print("Error sound played successfully.")
                return (f"Play sound: {error_sound_file.name}",)
            except Exception as e:
                print(f"Failed to play error sound: {str(e)}")
                return (f"Failed to play error sound: {str(e)}",)
        else:
            print("Error sound file not found.")
            return ("Error sound file not found.",)

    def start_timer(self, sound_directory, interval_minutes, volume):
        def timer_function():
            while True:
                self.BWIZ_NotificationSound(any, "always", volume, False, 0, False, sound_directory)  # Avoid recursion
                time.sleep(interval_minutes * 60)

        timer_thread = threading.Thread(target=timer_function)
        timer_thread.daemon = True
        timer_thread.start()

    def _play_sound(self, sound_file, volume):
        try:
            sound = AudioSegment.from_file(sound_file)
            sound = sound + (volume * 10 - 5)  # Adjust volume, ensure the calculation makes sense
            play(sound)
            print(f"Played sound: {sound_file}")
        except Exception as e:
            print(f"Error playing sound: {str(e)}")
            raise


    # Example usage
    if __name__ == "__main__":
        # Initialize the notification sound
        notification_sound = BWIZ_NotificationSound()
    
        # Call the play_sound method with appropriate arguments
        try:
            notification_sound.play_sound("/res/navi/navi1.mp3", 0.5)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
