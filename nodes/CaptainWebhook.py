import json
import os
import datetime
import requests
from server import PromptServer
import folder_paths

class CaptainWebhook:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.server = PromptServer.instance
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process_and_send"
    OUTPUT_NODE = True
    CATEGORY = "BWiZ"

    def process_and_send(self, images, filename=""):
        try:
            # Extract number from filename if it exists
            import re
            number_match = re.search(r'(\d+)', filename)
            number = number_match.group(1) if number_match else ""
            
            # Create webhook data
            webhook_data = {
                "status": "success",
                "filename": filename,
                "number": number,
                "timestamp": datetime.datetime.now().isoformat()
            }
            
            # Convert to JSON-serializable format
            webhook_data = {k: str(v) for k, v in webhook_data.items()}
            
            # Save webhook data with same number as image
            json_filename = f"webhook_data_{number}.json" if number else f"webhook_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            json_path = os.path.join(self.output_dir, json_filename)
            
            with open(json_path, 'w') as json_file:
                json.dump(webhook_data, json_file, indent=4)
            
            print(f"Webhook data saved: {json_path}")
            return (images,)
            
        except Exception as e:
            print(f"Error in webhook processing: {str(e)}")
            return (images,)

NODE_CLASS_MAPPINGS = {
    "BWIZ_CaptainWebhook": CaptainWebhook
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BWIZ_CaptainWebhook": "Captain Webhook 🪝"
}
