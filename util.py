# Hack: string type that is always equal in not equal comparisons
# Thanks to https://github.com/pythongosssss/ComfyUI-Custom-Scripts
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
