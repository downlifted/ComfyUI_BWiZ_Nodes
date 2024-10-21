from .BWIZ_CaptainWebhook import BWIZ_CaptainWebhook
from .BWIZ_AdvancedLoadImageBatch import BWIZ_AdvancedLoadImageBatch
from .BWIZ_NotificationSound import BWIZ_PlaySound 
from .BWIZ_ErrorDetector import BWIZ_ErrorDetector
from .BWIZ_HFRepoBatchLoader import BWIZ_HFRepoBatchLoader

NODE_CLASS_MAPPINGS = {
    "BWIZ_CaptainWebhook": BWIZ_CaptainWebhook,
    "BWIZ_AdvancedLoadImageBatch": BWIZ_AdvancedLoadImageBatch,
    "BWIZ_NotificationSound": BWIZ_PlaySound,
    "BWIZ_ErrorDetector": BWIZ_ErrorDetector,
    "BWIZ_HFRepoBatchLoader": BWIZ_HFRepoBatchLoader,

}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BWIZ_CaptainWebhook": "🧙🏼 BWIZ | Captain Webhook",
    "BWIZ_AdvancedLoadImageBatch": "🧙🏼 BWiZ | Batch Image Loader(Natural Increments)",
    "BWIZ_NotificationSound": "🧙🏼 BWiZ | Notification Sound (Navi)",
    "BWIZ_ErrorDetector": "🧙🏼 BWiZ | Error Detector (Notification)",
    "BWIZ_HFRepoBatchLoader": "🧙🏼 BWiZ | Batch Image Loader (HF Repo)",



}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']