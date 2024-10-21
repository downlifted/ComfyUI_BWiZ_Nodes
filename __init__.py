from .BWIZ_CaptainWebhook import BWIZ_CaptainWebhook
from .BWIZ_AdvancedLoadImageBatch import BWIZ_AdvancedLoadImageBatch
from .BWIZ_ErrorDetector import BWIZ_ErrorDetector
from .BWIZ_HFRepoBatchLoader import BWIZ_HFRepoBatchLoader
from .BWIZ_NotificationSound import BWIZ_NotificationSound


NODE_CLASS_MAPPINGS = {
    "BWIZ_CaptainWebhook": BWIZ_CaptainWebhook,
    "BWIZ_AdvancedLoadImageBatch": BWIZ_AdvancedLoadImageBatch,
    "BWIZ_ErrorDetector": BWIZ_ErrorDetector,
    "BWIZ_HFRepoBatchLoader": BWIZ_HFRepoBatchLoader,
    "BWIZ_NotificationSound": BWIZ_NotificationSound,

}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BWIZ_CaptainWebhook": "🧙🏼 BWIZ | Captain Webhook",
    "BWIZ_AdvancedLoadImageBatch": "🧙🏼 BWiZ | Batch Image Loader(Natural Increments)",
    "BWIZ_ErrorDetector": "🧙🏼 BWiZ | Error Detector (Notification)",
    "BWIZ_HFRepoBatchLoader": "🧙🏼 BWiZ | Batch Image Loader (HF Repo)",
    "BWIZ_NotificationSound": "🧙🏼 BWiZ | Notification Sound (Navi)",


}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']