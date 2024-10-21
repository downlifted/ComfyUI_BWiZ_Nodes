
# Example if uis is a list of lists
# Hack: string type that is always equal in not equal comparisons
from .util import AnyType

# Our any instance wants to be a wildcard string

class NotificationSound:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any": (AnyType('*'), {}),
                "mode": (["always", "on empty queue"], {}),
                "volume": ("FLOAT", {"min": 0, "max": 1, "step": 0.1, "default": 0.5}),
                "file": ("STRING", {"default": "navi1.mp3"})
            }
        }

    FUNCTION = "play_sound"
    OUTPUT_NODE = True
    RETURN_TYPES = ("*",)
    CATEGORY = "notifications"

    def play_sound(self, any, mode, volume, file):
        return {"ui": {"a": []}, "result": (0, )}




