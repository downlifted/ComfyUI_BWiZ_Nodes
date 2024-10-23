import threading
import time
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play
import json
import os
import requests

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")

class ErrorHandler:
    def __init__(self):
        self.errors = []
        self.lock = threading.Lock()

    def add_error(self, error):
        with self.lock:
            self.errors.append(error)

    def get_errors(self):
        with self.lock:
            return self.errors.copy()

    def clear_errors(self):
        with self.lock:
            self.errors.clear()

class InteractiveLogViewer:
    def __init__(self):
        self.sound_directory = Path(__file__).parent / "res" / "navi"
        self.error_keyword = "ERROR"
        self.log_file_path = None
        self.monitor_thread = None
        self.stop_monitoring = threading.Event()
        self.last_error_time = 0
        self.cooldown_period = 60  # Cooldown period in seconds
        self.log_buffer = []
        self.max_buffer_size = 100  # Maximum number of lines to keep in buffer
        self.error_handler = ErrorHandler()

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "input": (any, {}),
            "error_keyword": ("STRING", {"default": "ERROR", "multiline": False}),
            "log_file_path": ("STRING", {"default": "auto", "multiline": False}),
        }}

    RETURN_TYPES = ("BOOLEAN", "STRING", "HTML")
    RETURN_NAMES = ("error_detected", "log_path", "terminal_output")
    FUNCTION = "monitor_log"
    CATEGORY = "BWIZ/Log Monitoring"

    def find_log_file(self):
        possible_locations = [
            Path.cwd() / "ComfyUI" / "logs" / "comfyui.log",
            Path.cwd().parent / "ComfyUI" / "logs" / "comfyui.log",
            Path.cwd() / "logs" / "comfyui.log",
            Path.cwd().parent / "logs" / "comfyui.log",
        ]
        for location in possible_locations:
            if location.exists():
                return location
        return None

    def monitor_log(self, input, error_keyword, log_file_path):
        self.error_keyword = error_keyword
        
        if log_file_path.lower() == "auto":
            self.log_file_path = self.find_log_file()
            if not self.log_file_path:
                return (False, "Log file not found", self.generate_html_output("Log file not found. Please specify the path manually."))
        else:
            self.log_file_path = Path(log_file_path)
        
        if not self.log_file_path.exists():
            return (False, str(self.log_file_path), self.generate_html_output(f"Log file not found: {self.log_file_path}"))
        
        if not self.monitor_thread or not self.monitor_thread.is_alive():
            self.stop_monitoring.clear()
            self.monitor_thread = threading.Thread(target=self.monitor_log_file)
            self.monitor_thread.start()
        
        return (self.check_for_error(), str(self.log_file_path), self.generate_html_output())

    def check_for_error(self):
        try:
            with open(self.log_file_path, 'r') as log_file:
                log_content = log_file.read()
                if self.error_keyword.upper() in log_content.upper():
                    self.error_handler.add_error(f"Error detected: {self.error_keyword}")
                    return True
            return False
        except Exception as e:
            print(f"Error reading log file: {str(e)}")
            return False

    def monitor_log_file(self):
        while not self.stop_monitoring.is_set():
            try:
                with open(self.log_file_path, 'r') as log_file:
                    log_file.seek(0, 2)  # Move to the end of the file
                    while not self.stop_monitoring.is_set():
                        line = log_file.readline()
                        if not line:
                            time.sleep(0.1)  # Sleep briefly
                            continue
                        self.log_buffer.append(line.strip())
                        if len(self.log_buffer) > self.max_buffer_size:
                            self.log_buffer.pop(0)
                        if self.error_keyword.upper() in line.upper():
                            self.error_handler.add_error(line.strip())
                            self.play_error_sound()
                            self.trigger_alert(line.strip())
            except Exception as e:
                print(f"Error in monitor_log_file: {str(e)}")
                time.sleep(5)  # Wait before trying again

    def play_error_sound(self):
        current_time = time.time()
        if current_time - self.last_error_time > self.cooldown_period:
            error_sound_file = self.sound_directory / "error.mp3"
            if error_sound_file.exists():
                try:
                    sound = AudioSegment.from_file(error_sound_file)
                    play(sound)
                    self.last_error_time = current_time
                except Exception as e:
                    print(f"Failed to play error sound: {str(e)}")
            else:
                print("Error sound file not found.")

    def trigger_alert(self, error_message):
        # This method would be responsible for closing the error in ComfyUI
        # and queueing the next piece of art. As we don't have direct access
        # to ComfyUI's internals, we'll simulate this behavior.
        print(f"Alert triggered: {error_message}")
        print("Simulating error closure in ComfyUI...")
        print("Queueing next art piece...")
        
        # Here you would typically interact with ComfyUI's API or internal methods
        # to close the error and queue the next job. For demonstration, we'll
        # use a placeholder API call:
        try:
            requests.post('http://localhost:8188/queue', json={
                'prompt': 'next_art_piece',
                'close_error': True
            })
        except Exception as e:
            print(f"Failed to interact with ComfyUI: {str(e)}")

    def generate_html_output(self, error_message=None):
        if error_message:
            html_content = f"""
            <div style="color: red; font-family: sans-serif; padding: 10px;">
                <h3>Error:</h3>
                <p>{error_message}</p>
            </div>
            """
        else:
            html_content = f"""
            <div id="log-viewer" style="width: 100%; height: 300px; overflow-y: scroll; background-color: #000; color: #0f0; font-family: monospace; padding: 10px; border-radius: 5px;">
                <pre id="log-content"></pre>
            </div>
            <div id="error-list" style="margin-top: 10px; color: red;"></div>
            <script>
                const logViewer = document.getElementById('log-viewer');
                const logContent = document.getElementById('log-content');
                const errorList = document.getElementById('error-list');
                const logData = {json.dumps(self.log_buffer)};
                let errors = {json.dumps(self.error_handler.get_errors())};
                
                function updateLog() {{
                    logContent.textContent = logData.join('\\n');
                    logViewer.scrollTop = logViewer.scrollHeight;
                    errorList.innerHTML = '<h4>Detected Errors:</h4>' + errors.map(e => `<p>${{e}}</p>`).join('');
                }}
                
                updateLog();
                
                // Simulating periodic updates
                setInterval(() => {{
                    // In a real implementation, this would fetch new log data and errors from the server
                    const newEntry = `[${{new Date().toISOString()}}] Simulated log entry`;
                    logData.push(newEntry);
                    if (logData.length > 100) logData.shift();
                    if (Math.random() < 0.1) {{  // 10% chance of new error
                        errors.push(`New error at ${{new Date().toISOString()}}`);
                    }}
                    updateLog();
                }}, 2000);
            </script>
            """
        return html_content

    def __del__(self):
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.stop_monitoring.set()
            self.monitor_thread.join()

# This allows the class to be instantiated when the script is run directly
if __name__ == "__main__":
    log_viewer = InteractiveLogViewer()
    log_viewer.monitor_log(None, "ERROR", "auto")