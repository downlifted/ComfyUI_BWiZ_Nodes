# Hack: string type that is always equal in not equal comparisons
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


# Our any instance wants to be a wildcard string
any = AnyType("*")


class PlaySound:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "any": (any, {}),
            "mode": (["always", "on empty queue"], {}),
            "volume": ("FLOAT", {"min": 0, "max": 1, "step": 0.1, "default": 0.5}),
            "file": ("STRING", { "default": "notify.mp3" })
        }}

    FUNCTION = "bwiz_play_sound"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)
    OUTPUT_NODE = True
    RETURN_TYPES = (any,)

    CATEGORY = "utils"

    def IS_CHANGED(self, **kwargs):
        return float("NaN")

    def bwiz_play_sound(self, any, mode, volume, file):
        return {"ui": {"a": []}, "result": (any,)}


NODE_CLASS_MAPPINGS = {
    "BWIZ_NotificationSound": PlaySound,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BWIZ_NotificationSound": "🧙🏼 BWiZ | Notification Sound (Navi)",
}