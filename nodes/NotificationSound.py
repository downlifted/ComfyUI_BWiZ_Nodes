import os
import json
import folder_paths

class NotificationSound:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "trigger": ("*", {}),
                "mode": (["always", "on empty queue"], {"default": "always"}),
                "volume": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.1}),
                "file": ("STRING", {"default": "navi1.mp3"})
            }
        }

    RETURN_TYPES = ("*",)
    FUNCTION = "play_sound"
    OUTPUT_NODE = True
    CATEGORY = "BWIZ/Notifications"

    def play_sound(self, trigger, mode, volume, file):
        # Get the full path of the sound file
        sound_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sounds")
        full_path = os.path.join(sound_dir, file)

        # Check if the file exists
        if os.path.exists(full_path):
            # Send a signal to the client to play the sound
            data = json.dumps({
                "type": "notification_sound",
                "data": {
                    "file": file,
                    "volume": volume,
                    "mode": mode
                }
            })
            return {"ui": {"data": data}, "result": (trigger,)}
        else:
            print(f"Sound file not found: {full_path}")
            return {"result": (trigger,)}