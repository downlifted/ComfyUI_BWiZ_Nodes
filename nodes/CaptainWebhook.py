import os
import json
from PIL import Image
import torch
import numpy as np
import requests
import tempfile
from moviepy.editor import ImageSequenceClip
from datetime import datetime
from pathlib import Path
from .util import ComfyAnyType
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class CaptainWebhook:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "webhook_url": ("STRING", {"multiline": False, "default": 'http://localhost:5000/', "placeholder": "Webhook URL, or Discord Webhook URL"}),
                "input_filename": ("STRING", {"multiline": False, "default": '', "placeholder": "Filename prefix or full name, can be input."}),
                "input_image": ("IMAGE",),
                "message": ("STRING", {"multiline": True, "default": '', "placeholder": "Type Message Here(Or Convert to Input)"}),
                "timeout": ('FLOAT', {'default': 120, 'min': 10, 'max': 600}),
            },
            "optional": {
                "save_locally": (["false", "true"], {"default": "false"}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    OUTPUT_NODE = True
    FUNCTION = "process_and_send"
    CATEGORY = "BWIZ/Notifications"

    def process_and_send(self, webhook_url, input_filename, input_image, message, timeout, save_locally="false"):
        # ... (implementation details)        save_locally = (save_locally == 'true')

        if input_image is None:
            raise ValueError("No image provided")

        # Convert tensor to PIL Image
        pil_image = self.tensor_to_pil(input_image)

        # Determine filename
        if input_filename:
            filename = Path(input_filename)
            if not filename.suffix:
                filename = filename.with_suffix('.png')
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = Path(f"output_{timestamp}.png")

        # Determine output directory
        output_dir = Path(os.path.dirname(__file__)) / "outputs" if save_locally else Path(tempfile.gettempdir())
        output_dir.mkdir(parents=True, exist_ok=True)

        file_path = output_dir / filename

        # Save image
        pil_image.save(file_path)

        # Create JSON file with the same name as the image
        json_path = file_path.with_suffix('.json')
        metadata = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "filename": str(filename)
        }
        with open(json_path, 'w') as json_file:
            json.dump(metadata, json_file)

        # Upload to webhook
        with open(file_path, "rb") as image_file, open(json_path, "rb") as json_file:
            if webhook_url.startswith('https://discord.com/api/webhooks/'):
                # Discord webhook
                payload = {'content': message}
                files = {
                    'file': (filename.name, image_file),
                    'attachment': (json_path.name, json_file)
                }
                response = requests.post(webhook_url, data=payload, files=files, timeout=timeout)
            else:
                # Regular webhook
                files = {
                    'image': (filename.name, image_file),
                    'metadata': (json_path.name, json_file)
                }
                response = requests.post(webhook_url, files=files, timeout=timeout)

        result_message = f"Uploaded {filename.name} and {json_path.name}. Status: {response.status_code}"

        # Clean up temporary files if not saving locally
        if not save_locally:
            file_path.unlink()
            json_path.unlink()

        return (input_image, result_message)

    def tensor_to_pil(self, tensor):
        if tensor.dim() == 4:
            tensor = tensor.squeeze(0)
        if tensor.shape[0] == 1:
            tensor = tensor.squeeze(0)
        if tensor.dim() == 3 and tensor.shape[0] == 1:
            tensor = tensor.squeeze(0)

        # Normalize the tensor if it's not in the range [0, 255]
        if tensor.max() <= 1:
            tensor = (tensor * 255).clamp(0, 255)

        # Convert to 8-bit unsigned integer
        numpy_array = tensor.cpu().numpy().astype(np.uint8)

        # If the array is 2D, convert it to 3D
        if numpy_array.ndim == 2:
            numpy_array = numpy_array[:, :, np.newaxis]

        # If the array has only one channel, repeat it to create an RGB image
        if numpy_array.shape[2] == 1:
            numpy_array = np.repeat(numpy_array, 3, axis=2)

        return Image.fromarray(numpy_array)

def generate_and_upload(self, images, webhook_url: str, filename: str, frame_rate: int, save_locally: bool, message: str):
        output_dir = os.path.join(os.path.dirname(__file__), "outputs") if save_locally else tempfile.gettempdir()
        os.makedirs(output_dir, exist_ok=True)


        # Ensure filename has an extension
        if not os.path.splitext(filename)[1]:
            filename += '.png'

        file_path = os.path.join(output_dir, filename)

        # Save the image or video
        if len(images) == 1:
            pil_image = images[0].convert("RGB")
            pil_image.save(file_path)
        else:
            frames = [np.array(image.convert("RGB")) for image in images]
            clip = ImageSequenceClip(frames, fps=frame_rate)
            clip.write_videofile(file_path, codec="libx264", fps=frame_rate)

        # Create metadata file
        metadata_filename = f"{os.path.splitext(filename)[0]}_metadata.json"
        metadata_path = os.path.join(output_dir, metadata_filename)
        metadata = {
            "filename": filename,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        with open(metadata_path, 'w') as metadata_file:
            json.dump(metadata, metadata_file, indent=4)

        # Upload to webhook
        with open(file_path, "rb") as file_data:
            files = {
                "payload_json": (None, json.dumps({"content": message})),
                "file": (filename, file_data)
            }
            response = requests.post(webhook_url, files=files)

        result_message = f"Uploaded {filename}. Status: {response.status_code}"

        if not save_locally:
            os.remove(file_path)
            os.remove(metadata_path)

        return result_message

def create_metadata(self, filename, message, save_locally, file_path, webhook_url):  # Added webhook_url as a parameter
        # Define output_dir based on save_locally
        output_dir = os.path.join(os.path.dirname(__file__), "outputs") if save_locally else tempfile.gettempdir()
        os.makedirs(output_dir, exist_ok=True)

        metadata_filename = f"{os.path.splitext(filename)[0]}_metadata.json"
        metadata_path = os.path.join(output_dir, metadata_filename)
        metadata = {
            "filename": filename,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        with open(metadata_path, 'w') as metadata_file:
            json.dump(metadata, metadata_file, indent=4)

        # Upload to webhook
        with open(file_path, "rb") as file_data:
            files = {
                "payload_json": (None, json.dumps({ "content": message})),
                "file": (filename, file_data)
            }
            response = requests.post(webhook_url, files=files)

        result_message = f"Uploaded {filename}. Status: {response.status_code}"

        if not save_locally:
            os.remove(file_path)
            os.remove(metadata_path)

        return result_message

class CptnSendEmail:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any": (ComfyAnyType("*"), {}),
                "recipient": ("STRING", {'default': 'user@example.com'}),
                "subject": ('STRING', {'default': 'ComfyUI Notification'}),
                "body": ('STRING', {'default': 'Your task has completed.'}),
                "smtp_server": ('STRING', {'default': 'smtp.gmail.com'}),
                "smtp_port": ('INT', {'default': 587, 'min': 1, 'max': 65535}),
                "sender_email": ('STRING', {'default': 'sender@example.com'}),
                "sender_password": ('STRING', {'default': ''}),
            },
        }
    
    FUNCTION = 'send_email'
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    CATEGORY = "notifications"

    def send_email(self, any, recipient, subject, body, smtp_server, smtp_port, sender_email, sender_password):
        try:
            # Set up the MIME
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient
            message['Subject'] = subject

            # Add body to email
            message.attach(MIMEText(body, 'plain'))

            # Create SMTP session
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Enable security
                server.login(sender_email, sender_password)
                text = message.as_string()
                server.sendmail(sender_email, recipient, text)

            return ("Email sent successfully!",)
        except Exception as e:
            return (f"Failed to send email: {str(e)}",)

class CptnPushNoti:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "any": (ComfyAnyType("*"), {}),
                "device_token": ("STRING", {'default': ''}),
                "title": ('STRING', {'default': 'ComfyUI Notification'}),
                "message": ('STRING', {'default': 'Your task is complete.'}),
                "api_key": ('STRING', {'default': ''}),
            },
        }

    FUNCTION = 'send_push'
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    CATEGORY = "notifications"

    def send_push(self, any, device_token, title, message, api_key):
        try:
            # Firebase Cloud Messaging API endpoint
            url = "https://fcm.googleapis.com/fcm/send"

            # Headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"key={api_key}"
            }

            # Payload
            payload = {
                "to": device_token,
                "notification": {
                    "title": title,
                    "body": message
                }
            }

            # Send POST request
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                return ("Push notification sent successfully!",)
            else:
                return (f"Failed to send push notification. Status code: {response.status_code}",)
        except Exception as e:
            return (f"Failed to send push notification: {str(e)}",)
