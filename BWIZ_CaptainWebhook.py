import os
import json
from PIL import Image
import torch
import numpy as np
import requests
import tempfile
from moviepy.editor import ImageSequenceClip
from datetime import datetime
from pathlib import Path  # Add this import statement

class BWIZ_CaptainWebhook:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "webhook_url": ("STRING", {"multiline": False, "placeholder": "Webhook URL"}),
                "input_filename": ("STRING", {"multiline": False, "placeholder": "Input filename"}),
                "file_type": (["image", "video"],),
                "text_data": ("STRING", {"multiline": True, "placeholder": "Text data for Discord message or file content"}),
                "input_image": ("IMAGE",),
            },
            "optional": {
                "frame_rate": ("INT", {"default": 12, "min": 1, "max": 60, "step": 1}),
                "save_locally": (["false", "true"],),
                "bot_username": ("STRING", {"default": "ComfyUI Bot"}),
            }
        }
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "filename")
    FUNCTION = "process_and_send"
    CATEGORY = "BWIZ Nodes/Webhook"
    def process_and_send(self, webhook_url='', input_filename='', file_type='image', text_data='', input_image=None, frame_rate=12, save_locally='false', bot_username='ComfyUI Bot'):
        save_locally = (save_locally == 'true')

        if input_image is None:
            raise Exception("No image provided")

        # Check if input_image is already a PIL Image
        if isinstance(input_image, Image.Image):
            pil_image = input_image
        else:
            pil_image = self.tensor_to_pil(input_image)

        # Use input_filename as the base for the output filename
        if not input_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"output_{timestamp}.png"  # Ensure default extension is .png
        else:
            filename = Path(input_filename).stem
            filename = f"{filename}.png" if file_type == 'image' else f"{filename}.mp4"

        # Determine output directory
        output_dir = Path(os.path.dirname(__file__)) / "outputs" if save_locally else Path(tempfile.gettempdir())
        output_dir.mkdir(parents=True, exist_ok=True)

        file_path = output_dir / filename

        # Save the image or create video
        if file_type == 'image':
            pil_image = pil_image.convert("RGB")
            pil_image.save(file_path)
        else:  # video
            frames = [np.array(pil_image.convert("RGB"))]
            clip = ImageSequenceClip(frames, fps=frame_rate)
            clip.write_videofile(str(file_path), codec="libx264", fps=frame_rate)

        # Create and save metadata
        metadata_path = output_dir / f"{Path(filename).stem}_metadata.json"
        with open(metadata_path, 'w') as f:
            f.write(text_data)

        print(f"Metadata saved at: {metadata_path}")
        # Upload to webhook
        with open(file_path, "rb") as file_data:
            files = {
                "payload_json": (None, json.dumps({"username": bot_username, "content": text_data})),
                "file": (filename, file_data)
            }
            response = requests.post(webhook_url, files=files)

        result_message = f"Uploaded {filename}. Status: {response.status_code}"

        # Clean up temporary files if not saving locally
        if not save_locally:
            file_path.unlink()
            # Comment out or remove the following line to keep the JSON file
            # metadata_path.unlink()

        print(f"JSON metadata file remains at: {metadata_path}")

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
    def generate_and_upload(self, images, webhook_url: str, filename: str, frame_rate: int, save_locally: bool, bot_username: str, message: str):
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
            "bot_username": bot_username,
            "timestamp": datetime.now().isoformat()
        }
        with open(metadata_path, 'w') as metadata_file:
            json.dump(metadata, metadata_file, indent=4)

        # Upload to webhook
        with open(file_path, "rb") as file_data:
            files = {
                "payload_json": (None, json.dumps({"username": bot_username, "content": message})),
                "file": (filename, file_data)
            }
            response = requests.post(webhook_url, files=files)

        result_message = f"Uploaded {filename}. Status: {response.status_code}"

        if not save_locally:
            os.remove(file_path)
            os.remove(metadata_path)

        return result_message

    def create_metadata(self, filename, message, bot_username, save_locally, file_path, webhook_url):  # Added webhook_url as a parameter
        # Define output_dir based on save_locally
        output_dir = os.path.join(os.path.dirname(__file__), "outputs") if save_locally else tempfile.gettempdir()
        os.makedirs(output_dir, exist_ok=True)

        metadata_filename = f"{os.path.splitext(filename)[0]}_metadata.json"
        metadata_path = os.path.join(output_dir, metadata_filename)
        metadata = {
            "filename": filename,
            "message": message,
            "bot_username": bot_username,
            "timestamp": datetime.now().isoformat()
        }
        with open(metadata_path, 'w') as metadata_file:
            json.dump(metadata, metadata_file, indent=4)

        # Upload to webhook
        with open(file_path, "rb") as file_data:
            files = {
                "payload_json": (None, json.dumps({"username": bot_username, "content": message})),
                "file": (filename, file_data)
            }
            response = requests.post(webhook_url, files=files)

        result_message = f"Uploaded {filename}. Status: {response.status_code}"

        if not save_locally:
            os.remove(file_path)
            os.remove(metadata_path)

        return result_message

