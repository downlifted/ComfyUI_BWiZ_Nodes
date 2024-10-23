import os
import json
from PIL import Image
import torch
import numpy as np
import requests
import tempfile
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from datetime import datetime
from pathlib import Path
from .util import ComfyAnyType
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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