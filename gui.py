import tkinter as tk
import threading
import subprocess
import webbrowser
import ctypes
from datetime import datetime
import pyautogui

from stt import listen
from llm import ask_ai
from tts import speak


class VoiceAssistantGUI:

    def __init__(self, window):
        self.window = window
        self.window.title("AI Voice Assistant")
        self.window.geometry("850x700")
        self.window.resizable(False, False)

        self.running = True
        self.active = False

        # Header
        header = tk.Frame(window)
        header.pack(fill="x", pady=20)

        title = tk.Label(
            header,
            text="AI Voice Assistant",
            font=("Arial", 28, "bold")
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="Your Personal Desktop Assistant",
            font=("Arial", 12)
        )
        subtitle.pack(pady=5)

        # Status
        self.status = tk.Label(
            window,
            text="● Sleeping",
            font=("Arial", 18, "bold")
        )
        self.status.pack(pady=15)

        # Conversation area
        chat_frame = tk.Frame(window)
        chat_frame.pack(padx=40, pady=10, fill="both", expand=True)

        self.chat = tk.Text(
            chat_frame,
            height=18,
            width=85,
            font=("Arial", 12),
            wrap="word",
            state="disabled"
        )
        self.chat.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            chat_frame,
            command=self.chat.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.chat.config(yscrollcommand=scrollbar.set)

        # Buttons
        button_frame = tk.Frame(window)
        button_frame.pack(pady=20)

        self.start_button = tk.Button(
            button_frame,
            text="▶ Start Assistant",
            font=("Arial", 13, "bold"),
            width=18,
            command=self.start_assistant
        )
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = tk.Button(
            button_frame,
            text="■ Stop",
            font=("Arial", 13, "bold"),
            width=12,
            command=self.stop_assistant
        )
        self.stop_button.grid(row=0, column=1, padx=10)

        self.close_button = tk.Button(
            button_frame,
            text="✕ Close",
            font=("Arial", 13),
            width=12,
            command=self.close
        )
        self.close_button.grid(row=0, column=2, padx=10)

        # Clock
        self.clock = tk.Label(
            window,
            text="",
            font=("Arial", 11)
        )
        self.clock.pack(pady=5)

        # Developer name
        credit = tk.Label(
            window,
            text="Developed by Abubakkar Cheema",
            font=("Arial", 9)
        )
        credit.pack(pady=5)

        self.update_clock()

    def update_clock(self):
        current_time = datetime.now().strftime(
            "%A, %B %d, %Y   |   %I:%M:%S %p"
        )

        self.clock.config(text=current_time)

        if self.running:
            self.window.after(1000, self.update_clock)

    def add_message(self, speaker, message):
        self.chat.config(state="normal")

        self.chat.insert(
            tk.END,
            f"{speaker}: {message}\n\n"
        )

        self.chat.see(tk.END)

        self.chat.config(state="disabled")

    def update_status(self, text):
        self.window.after(
            0,
            lambda: self.status.config(text=text)
        )

    def start_assistant(self):
        if not self.running:
            return

        self.start_button.config(state="disabled")
        self.active = False

        threading.Thread(
            target=self.assistant_loop,
            daemon=True
        ).start()

    def stop_assistant(self):
        self.active = False
        self.update_status("● Sleeping")
        self.add_message(
            "System",
            "Assistant is sleeping."
        )

    def open_command(self, command):

        apps = {
            "calculator": "calc.exe",
            "notepad": "notepad.exe",
            "paint": "mspaint.exe",
            "task manager": "taskmgr.exe",
            "file explorer": "explorer.exe",
            "explorer": "explorer.exe",
            "vs code": r"C:\Users\abuba\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            "visual studio code": r"C:\Users\abuba\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        }

        websites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "gmail": "https://mail.google.com",
            "chatgpt": "https://chatgpt.com",
        }

        for name, program in apps.items():

            if name in command:
                speak(f"Opening {name}.")
                self.add_message(
                    "Assistant",
                    f"Opening {name}."
                )
                subprocess.Popen(program)
                return True

        for name, url in websites.items():

            if name in command:
                speak(f"Opening {name}.")
                self.add_message(
                    "Assistant",
                    f"Opening {name}."
                )
                webbrowser.open(url)
                return True

        return False

    def assistant_loop(self):

        speak(
            "Hello! Say Hey Assistant when you need me."
        )

        self.add_message(
            "Assistant",
            "Hello! Say Hey Assistant when you need me."
        )

        while self.running:

            self.update_status("● Listening...")

            user_text = listen()

            if not user_text:
                continue

            self.add_message(
                "You",
                user_text
            )

            user_text = user_text.lower().strip()

            # Wake word
            if not self.active:

                if "hey assistant" in user_text:

                    self.active = True

                    self.update_status("● Active")

                    speak(
                        "Yes, how can I help?"
                    )

                    self.add_message(
                        "Assistant",
                        "Yes, how can I help?"
                    )

                continue

            # Exit
            if user_text in ["exit", "quit", "stop"]:

                speak("Goodbye!")

                self.add_message(
                    "Assistant",
                    "Goodbye!"
                )

                self.running = False
                break

            # Sleep
            if user_text in [
                "go to sleep",
                "sleep",
                "stop listening"
            ]:

                speak(
                    "Okay, I am going to sleep."
                )

                self.add_message(
                    "Assistant",
                    "Okay, I am going to sleep."
                )

                self.active = False
                self.update_status("● Sleeping")

                continue

            # Open apps/websites
            if self.open_command(user_text):
                continue

            # Time
            if (
                "what time is it" in user_text
                or "current time" in user_text
            ):

                current_time = datetime.now().strftime(
                    "%I:%M %p"
                )

                response = (
                    f"The current time is {current_time}."
                )

                self.add_message(
                    "Assistant",
                    response
                )

                speak(response)

                continue

            # Date
            if (
                "today" in user_text
                and "date" in user_text
            ):

                current_date = datetime.now().strftime(
                    "%A, %B %d, %Y"
                )

                response = f"Today is {current_date}."

                self.add_message(
                    "Assistant",
                    response
                )

                speak(response)

                continue

            # Volume up
            if "volume up" in user_text:

                speak("Increasing volume.")

                self.add_message(
                    "Assistant",
                    "Increasing volume."
                )

                for _ in range(5):

                    ctypes.windll.user32.keybd_event(
                        0xAF, 0, 0, 0
                    )

                    ctypes.windll.user32.keybd_event(
                        0xAF, 0, 2, 0
                    )

                continue

            # Volume down
            if "volume down" in user_text:

                speak("Decreasing volume.")

                self.add_message(
                    "Assistant",
                    "Decreasing volume."
                )

                for _ in range(5):

                    ctypes.windll.user32.keybd_event(
                        0xAE, 0, 0, 0
                    )

                    ctypes.windll.user32.keybd_event(
                        0xAE, 0, 2, 0
                    )

                continue

            # Mute
            if "mute" in user_text:

                speak("Muting volume.")

                self.add_message(
                    "Assistant",
                    "Muting volume."
                )

                ctypes.windll.user32.keybd_event(
                    0xAD, 0, 0, 0
                )

                ctypes.windll.user32.keybd_event(
                    0xAD, 0, 2, 0
                )

                continue

            # Screenshot
            if (
                "take a screenshot" in user_text
                or "take screenshot" in user_text
            ):

                screenshot = pyautogui.screenshot()

                filename = datetime.now().strftime(
                    "screenshot_%Y%m%d_%H%M%S.png"
                )

                path = rf"C:\Users\abuba\Desktop\{filename}"

                screenshot.save(path)

                response = (
                    "Screenshot taken and saved on your desktop."
                )

                self.add_message(
                    "Assistant",
                    response
                )

                speak(response)

                continue

            # AI
            self.update_status("● Thinking...")

            response = ask_ai(user_text)

            self.add_message(
                "Assistant",
                response
            )

            speak(response)

            self.update_status("● Active")

        self.update_status("● Stopped")

        self.window.after(
            0,
            lambda: self.start_button.config(
                state="normal"
            )
        )

    def close(self):

        self.running = False
        self.window.destroy()


if __name__ == "__main__":

    window = tk.Tk()

    app = VoiceAssistantGUI(window)

    window.mainloop()