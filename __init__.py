from .nodes.CaptainWebhook import CptnWebhook
from .nodes.CaptainWebhook import CptnSendEmail
from .nodes.CaptainWebhook import CptnPushNoti
from .nodes.AdvancedLoadImageBatch import AdvancedLoadImageBatch
from .nodes.ErrorDetector import ErrorDetector
from .nodes.HFRepoBatchLoader import HFRepoBatchLoader
from .nodes.NotificationSound import NotificationSound


NODE_CLASS_MAPPINGS = {
    "CaptainWebhook": CptnWebhook,
    "CaptainWebhook-Email": CptnSendEmail,
    "CaptainWebhook-Push": CptnPushNoti,
    "BWIZ_AdvancedLoadImageBatch": AdvancedLoadImageBatch,
    "BWIZ_ErrorDetector": ErrorDetector,
    "BWIZ_HFRepoBatchLoader": HFRepoBatchLoader,
    "BWIZ_NotificationSound": NotificationSound,

}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CptnWebhook": "🧙🏼 BWIZ | Captain Webhook(Hook)",
    "AdvancedLoadImageBatch": "🧙🏼 BWiZ | Batch Image Loader(Natural Increments)",
    "ErrorDetector": "🧙🏼 BWiZ | Error Detector (Notification)",
    "HFRepoBatchLoader": "🧙🏼 BWiZ | Batch Image Loader (HF Repo)",
    "NotificationSound": "🧙🏼 BWiZ | Notification Sound (Navi)",
    "CptnSendEmail": "🧙🏼 BWIZ | Captain Webhook(Email)",
    "CptnPushNoti": "🧙🏼 BWIZ | Captain Webhook(Push Notffication)",



}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']