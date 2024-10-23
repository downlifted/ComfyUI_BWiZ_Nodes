import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import ssl
import numpy as np
from PIL import Image
import io
import torch

class BWIZSendEmail:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "recipient": ("STRING", {'default': 'user@example.com'}),
                "subject": ('STRING', {'default': 'ComfyUI Notification'}),
                "body": ('STRING', {'default': 'Your task has completed.'}),
                "smtp_server": ('STRING', {'default': 'smtp.gmail.com'}),
                "smtp_port": ('INT', {'default': 587, 'min': 1, 'max': 65535}),
                "sender_email": ('STRING', {'default': 'sender@example.com'}),
                "sender_password": ('STRING', {'default': ''}),
                "use_tls": ("BOOLEAN", {'default': True}),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "send_email"
    OUTPUT_NODE = True
    CATEGORY = "BWiz/Notifications"

    def send_email(self, image, recipient, subject, body, smtp_server, smtp_port, sender_email, sender_password, use_tls):
        try:
            # Set up the MIME
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient
            message['Subject'] = subject

            # Add body to email
            message.attach(MIMEText(body, 'plain'))

            # Process and attach the image
            if isinstance(image, torch.Tensor):
                # Convert PyTorch tensor to numpy array
                image_np = image.cpu().numpy()
            elif isinstance(image, np.ndarray):
                image_np = image
            else:
                raise ValueError(f"Unsupported image type: {type(image)}")

            # Handle various image shapes
            if len(image_np.shape) == 4:
                if image_np.shape[0] == 1:  # Single image in a batch
                    image_np = image_np[0]
                else:
                    raise ValueError(f"Unsupported batch size: {image_np.shape[0]}")
            
            if len(image_np.shape) == 3:
                if image_np.shape[2] == 3:  # (H, W, 3) format
                    pass
                elif image_np.shape[0] == 3:  # (3, H, W) format
                    image_np = np.transpose(image_np, (1, 2, 0))
                else:
                    raise ValueError(f"Unsupported image shape: {image_np.shape}")
            else:
                raise ValueError(f"Unsupported image shape: {image_np.shape}")

            # Ensure the image is in the correct range [0, 255] and type uint8
            if image_np.dtype != np.uint8:
                image_np = np.clip(image_np * 255, 0, 255).astype(np.uint8)

            pil_image = Image.fromarray(image_np)
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            image_mime = MIMEImage(img_byte_arr)
            image_mime.add_header('Content-Disposition', 'attachment', filename='comfyui_image.png')
            message.attach(image_mime)

            # Create SMTP session
            if use_tls:
                context = ssl.create_default_context()
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls(context=context)
                    server.login(sender_email, sender_password)
                    text = message.as_string()
                    server.sendmail(sender_email, recipient, text)
            else:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.login(sender_email, sender_password)
                    text = message.as_string()
                    server.sendmail(sender_email, recipient, text)

            return ("Email sent successfully with the attached image!",)
        except smtplib.SMTPAuthenticationError:
            return ("Failed to send email: Authentication failed. Please check your email and password.",)
        except ssl.SSLError as e:
            return (f"Failed to send email: SSL/TLS error. Error details: {str(e)}",)
        except smtplib.SMTPException as e:
            return (f"Failed to send email: SMTP error. Error details: {str(e)}",)
        except Exception as e:
            return (f"Failed to send email: Unexpected error. Error details: {str(e)}",)