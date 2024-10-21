import os
import glob
import random
import requests
from PIL import Image, ImageOps
from io import BytesIO
import numpy as np
import torch
import re
from huggingface_hub import hf_hub_url  # Import for Hugging Face

class BWIZ_HFRepoBatchLoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "repo_id": ("STRING", {"default": "", "placeholder": "Hugging Face Repo ID (e.g., 'bewiz/testimages')"}),
                "hf_token": ("STRING", {"default": "", "placeholder": "Hugging Face API token (required for private repos)"}),
                "output_dir": ("STRING", {"default": "", "placeholder": "Output directory (optional)"}),
                "sort_order": (["numerical", "alphabetical", "random"],),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "BOOLEAN", "STRING")
    RETURN_NAMES = ("images", "masks", "has_image", "status")
    FUNCTION = "load_images"
    CATEGORY = "Image"

    def load_images(self, repo_id, hf_token, output_dir="", sort_order='numerical'):
        image_urls = self.get_image_urls_from_directory(repo_id, hf_token)
        if not image_urls:
            print("No images found in the specified Hugging Face repository.")
            return None, None, False, "No images found"

        image_urls = self.sort_images(image_urls, sort_order)
        images, masks = self.load_images_from_url(image_urls, output_dir)

        status_message = f"Downloaded {len(images)} images from {repo_id}"
        return images, masks, True, status_message

    def get_image_urls_from_directory(self, repo_id, hf_token):
        """Fetches image URLs from a Hugging Face repository."""
        image_urls = []
        headers = {"Authorization": f"Bearer {hf_token}"} if hf_token else {}

        try:
            api_url = f"https://huggingface.co/api/v4/models/{repo_id}/files-and-versions"
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()

            file_data = response.json()

            for item in file_data["siblings"]:
                if item["rfilename"].endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp")):
                    image_urls.append(hf_hub_url(
                        repo_id=repo_id, revision="main", filename=item["rfilename"]
                    ))

        except Exception as e:
            print(f"Failed to fetch images from Hugging Face repository: {e}")

        return image_urls

    def sort_images(self, image_urls, sort_order):
        if sort_order == "numerical":
            return sorted(image_urls, key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else float('inf'))
        elif sort_order == "alphabetical":
            return sorted(image_urls)
        elif sort_order == "random":
            random.shuffle(image_urls)
            return image_urls

    def load_images_from_url(self, urls, output_dir, keep_alpha_channel=False):
        images = []
        masks = []

        if not output_dir:
            output_dir = os.path.join("output", re.sub(r"[^a-zA-Z0-9]+", "_", urls[0].split("/")[-2]))
        os.makedirs(output_dir, exist_ok=True)

        for i, url in enumerate(urls):
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
                img = ImageOps.exif_transpose(img)
                has_alpha = "A" in img.getbands()
                mask = None

                if "RGB" not in img.mode:
                    img = img.convert("RGBA") if has_alpha else img.convert("RGB")

                if has_alpha:
                    mask = img.getchannel("A")
                    alpha = img.split()[-1]
                    image = Image.new("RGB", img.size, (0, 0, 0))
                    image.paste(img, mask=alpha)
                    image.putalpha(alpha)

                    if not keep_alpha_channel:
                        image = image.convert("RGB")
                    else:
                        image = img

                images.append(self.pil2tensor(image))
                masks.append(self.pil2tensor(mask, mode="L") if mask else torch.zeros((64, 64), dtype=torch.float32, device="cpu"))

                # Save the image
                img.save(os.path.join(output_dir, f"{i:05d}.png"))

            except Exception as e:
                print(f"Failed to download image from {url}: {str(e)}")

        return images, masks

    def check_image_sizes(self, images):
        base_size = images[0].shape[1:3]
        return all(image.shape[1:3] == base_size for image in images)

    def pil2tensor(self, image, mode="RGB"):
        if image is None:
            return torch.zeros((1, 64, 64, 3), dtype=torch.float32, device="cpu")
        image = np.array(image).astype(np.float32) / 255.0
        if mode == "L":
            image = image[:, :, np.newaxis]
        return torch.from_numpy(image).permute(2, 0, 1).unsqueeze(0)