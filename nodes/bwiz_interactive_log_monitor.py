import os
import time
import threading
from queue import Queue
import json
from pathlib import Path
import pygame

class InteractiveLogMonitor:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "log_file_path": ("STRING", {"default": "auto"}),
                "error_keyword": ("STRING", {"default": "ERROR"}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "monitor_logs"
    OUTPUT_NODE = True
    CATEGORY = "BWIZ/Log Monitoring"

    def __init__(self):
        self.log_file_path = None
        self.error_keyword = "ERROR"
        self.log_queue = Queue()
        self.stop_event = threading.Event()
        self.monitor_thread = None
        self.last_error_time = 0
        self.cooldown_period = 60  # seconds
        pygame.mixer.init()
        self.error_sound = pygame.mixer.Sound(str(Path(__file__).parent / "res" / "js" / "assets" / "error.mp3"))

    def find_log_file(self):
        possible_locations = [
            Path.cwd() / "ComfyUI" / "logs" / "comfyui.log",
            Path.cwd().parent / "ComfyUI" / "logs" / "comfyui.log",
            Path.cwd() / "logs" / "comfyui.log",
            Path.cwd().parent / "logs" / "comfyui.log",
        ]
        for location in possible_locations:
            if location.exists():
                return str(location)
        return None

    def monitor_logs(self, log_file_path, error_keyword):
        self.error_keyword = error_keyword
        if log_file_path.lower() == "auto":
            self.log_file_path = self.find_log_file()
        else:
            self.log_file_path = log_file_path

        if not self.log_file_path or not os.path.exists(self.log_file_path):
            return ("Log file not found",)

        if self.monitor_thread is None or not self.monitor_thread.is_alive():
            self.stop_event.clear()
            self.monitor_thread = threading.Thread(target=self.log_monitor_thread)
            self.monitor_thread.start()

        return (self.generate_output(),)

    def log_monitor_thread(self):
        with open(self.log_file_path, 'r') as log_file:
            log_file.seek(0, 2)  # Move to the end of the file
            while not self.stop_event.is_set():
                line = log_file.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                self.log_queue.put(line.strip())
                if self.error_keyword.upper() in line.upper():
                    self.handle_error(line.strip())

    def handle_error(self, error_message):
        current_time = time.time()
        if current_time - self.last_error_time > self.cooldown_period:
            self.error_sound.play()
            self.last_error_time = current_time
        print(f"Error detected: {error_message}")
        # Here you would typically interact with ComfyUI to handle the error and queue the next image
        # For demonstration, we'll just print a message
        print("Simulating error handling and queueing next image in ComfyUI")

    def generate_output(self):
        logs = []
        while not self.log_queue.empty():
            logs.append(self.log_queue.get())
        
        html_output = f"""
        <div id="log-monitor" style="width: 100%; height: 400px; overflow-y: scroll; background-color: #000; color: #0f0; font-family: monospace; padding: 10px; border-radius: 5px;">
            <pre id="log-content"></pre>
        </div>
        <script>
            const logMonitor = document.getElementById('log-monitor');
            const logContent = document.getElementById('log-content');
            let logs = {json.dumps(logs)};
            
            function updateLogs() {{
                logContent.textContent = logs.join('\\n');
                logMonitor.scrollTop = logMonitor.scrollHeight;
            }}
            
            updateLogs();
            
            // Simulating real-time updates
            setInterval(() => {{
                fetch('/bwiz_log_monitor_update')
                    .then(response => response.json())
                    .then(data => {{
                        logs = logs.concat(data.new_logs);
                        if (logs.length > 100) logs = logs.slice(-100);
                        updateLogs();
                    }});
            }}, 1000);
        </script>
        """
        return html_output

    def __del__(self):
        self.stop_event.set()
        if self.monitor_thread:
            self.monitor_thread.join()

NODE_CLASS_MAPPINGS = {
    "BWIZInteractiveLogMonitor": InteractiveLogMonitor
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BWIZInteractiveLogMonitor": "BWIZ Interactive Log Monitor"
}