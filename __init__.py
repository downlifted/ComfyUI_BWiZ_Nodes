from .nodes.CaptainWebhook import CaptainWebhook
from .nodes.ComfyEmail import BWIZSendEmail
from .nodes.AdvancedLoadImageBatch import AdvancedLoadImageBatch
from .nodes.ErrorDetector import InteractiveLogViewer
from .nodes.HFRepoBatchLoader import HFRepoBatchLoader
from .nodes.NotificationSound import NotificationSound


NODE_CLASS_MAPPINGS = {
    "BWIZ_CaptainWebhook": CaptainWebhook,
    "BWIZ_ComfyEmail": BWIZSendEmail,
    "BWIZ_AdvancedLoadImageBatch": AdvancedLoadImageBatch,
    "BWIZ_ErrorDetector": InteractiveLogViewer,
    "BWIZ_HFRepoBatchLoader": HFRepoBatchLoader,
    "BWIZ_NotificationSound": NotificationSound,

}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BWIZ_CaptainWebhook": "🧙🏼 BWIZ | Captain Webhook",
    "BWIZ_AdvancedLoadImageBatch": "🧙🏼 BWiZ | Batch Image Loader(Natural Increments)",
    "BWIZ_ErrorDetector": "🧙🏼 BWiZ | Error Detector/Alert (Log Viewer)",
    "BWIZ_HFRepoBatchLoader": "🧙🏼 BWiZ | Batch Image Loader (HF Repo)",
    "BWIZ_NotificationSound": "🧙🏼 BWiZ | Notification Sound",
    "BWIZ_CaptainWebhook-Email": "🧙🏼 BWIZ | Captain Webhook(Email)",



}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']