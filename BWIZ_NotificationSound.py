# Hack: string type that is always equal in not equal comparisons
from .util import AnyType

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


# Our any instance wants to be a wildcard string
any = AnyType("*")


class BWIZ_NotificationSound:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "any": (any, {}),
            "mode": (["always", "on empty queue"], {}),
            "volume": ("FLOAT", {"min": 0, "max": 1, "step": 0.1, "default": 0.5}),
            "file": ("STRING", { "default": "navi1.mp3" })
        }}

    FUNCTION = "BWIZ_NotificationSound"
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)
    OUTPUT_NODE = True
    RETURN_TYPES = (any,)

    CATEGORY = "BWIZ/utils"

    def IS_CHANGED(self, **kwargs):
        return float("NaN")

    def BWIZ_NotificationSound(self, any, mode, volume, file):
        return {"ui": {"play_sound": True, "file": file, "volume": volume}, "result": (any,)}

