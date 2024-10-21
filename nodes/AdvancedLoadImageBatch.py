import os
import glob
import random
import requests
from PIL import Image, ImageOps
from io import BytesIO
import numpy as np
import torch

class AdvancedLoadImageBatch:
    current_index = 0  # Class-level variable to track the current index

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF, "step": 1}),
                "max_value": ("INT", {"default": 10, "min": 1, "max": 0xFFFFFFFFFFFFFFFF, "step": 1}),
                "path": ("STRING", {"default": '', "multiline": False}),
                "natural_sort": (["true", "false"],),
                "path_type": (["directory", "url_directory"],),
                "sort_order": (["numerical", "alphabetical", "creation_date", "random"],),
            },
            "optional": {
                "filename_text_extension": (["true", "false"],),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "INT", "INT", "INT")
    RETURN_NAMES = ("image", "filename_text", "current_index", "width", "height")
    FUNCTION = "load_batch_images"
    CATEGORY = "BWIZ Nodes/Images"

    def load_batch_images(self, seed, max_value, path, natural_sort='true', path_type='directory', sort_order='numerical', filename_text_extension='true'):
        natural_sort = (natural_sort == 'true')
        is_url_dir = (path_type == 'url_directory')

        if not os.path.exists(path) and not is_url_dir:
            print(f"Path does not exist: {path}")
            return (None, None, None, None, None)

        fl = self.NaturalSortLoader(path, sort_order, is_url_dir)

        # Determine image selection based on sort_order
        if sort_order == 'random':
            AdvancedLoadImageBatch.current_index = random.randint(0, len(fl.image_paths) - 1)
        else:
            AdvancedLoadImageBatch.current_index = seed % len(fl.image_paths)  # Ensure index wraps around

        image, filename = fl.get_image_by_id(AdvancedLoadImageBatch.current_index)

        # Increment the index for the next run
        AdvancedLoadImageBatch.current_index = (AdvancedLoadImageBatch.current_index + 1) % max_value

        if image is None:
            print(f"No valid image was found for the given parameters.")
            return (None, None, None, None, None)

        # Convert PIL Image to tensor
        image_np = np.array(image).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np).unsqueeze(0)

        if filename_text_extension == "false":
            filename = os.path.splitext(filename)[0]

        width, height = image.size

        return (image_tensor, filename, AdvancedLoadImageBatch.current_index, width, height)

    class NaturalSortLoader:
        def __init__(self, directory_path, sort_order, is_url_dir):
            self.image_paths = []
            self.index = 0
            self.load_images(directory_path, is_url_dir)
            self.sort_images(sort_order)

        def sort_images(self, sort_order):
            if sort_order == "numerical":
                self.image_paths.sort(key=lambda x: int(''.join(filter(str.isdigit, x))) if any(char.isdigit() for char in x) else float('inf'))
            elif sort_order == "alphabetical":
                self.image_paths.sort()
            elif sort_order == "creation_date":
                self.image_paths.sort(key=os.path.getctime)
            elif sort_order == "random":
                random.shuffle(self.image_paths)

        def load_images(self, directory_path, is_url_dir):
            if is_url_dir:
                # Implement logic to load images from a URL directory
                image_urls = self.get_image_urls_from_directory(directory_path)
                for url in image_urls:
                    try:
                        response = requests.get(url)
                        if response.status_code == 200:
                            image = Image.open(BytesIO(response.content))
                            self.image_paths.append((url, image))
                    except Exception as e:
                        print(f"Failed to load image from {url}: {e}")
            else:
                for file_name in glob.glob(os.path.join(glob.escape(directory_path), '*'), recursive=True):
                    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.bmp')):
                        abs_file_path = os.path.abspath(file_name)
                        self.image_paths.append(abs_file_path)

        def get_image_urls_from_directory(self, directory_url):
            # Implement logic to retrieve image URLs from the directory URL
            # This is a placeholder function and needs to be implemented
            return []

        def get_image_by_id(self, image_id):
            if image_id < 0 or image_id >= len(self.image_paths):
                print(f"Invalid image index `{image_id}`")
                return None, None

            if isinstance(self.image_paths[image_id], tuple):
                # If the image is from a URL, it's stored as a tuple (url, image)
                url, image = self.image_paths[image_id]
                return image, url
            else:
                # If the image is from a local path
                i = Image.open(self.image_paths[image_id])
                i = ImageOps.exif_transpose(i)
                return i, os.path.basename(self.image_paths[image_id])

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        fl = AdvancedLoadImageBatch.NaturalSortLoader(kwargs['path'], kwargs['sort_order'], kwargs['path_type'] == 'url_directory')
        filename = os.path.basename(fl.image_paths[0])
        image = os.path.join(kwargs['path'], filename)
        return os.path.getmtime(image)