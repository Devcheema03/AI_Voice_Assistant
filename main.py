import subprocess
import webbrowser
from datetime import datetime
import ctypes
import pyautogui

from stt import listen
from llm import ask_ai
from tts import speak


def open_command(command):
    command = command.lower().strip()

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
            subprocess.Popen(program)
            return True

    for name, url in websites.items():
        if name in command:
            speak(f"Opening {name}.")
            webbrowser.open(url)
            return True

    return False


def main():
    print("AI Voice Assistant started!")
    speak("Hello! Say Hey Assistant when you need me.")

    active = False

    while True:
        user_text = listen()

        if not user_text:
            continue

        user_text = user_text.lower().strip()

        if not active:
            if "hey assistant" in user_text:
                active = True
                speak("Yes, how can I help?")
            else:
                print("Waiting for wake word...")
            continue

        if user_text in ["exit", "quit", "stop"]:
            speak("Goodbye!")
            break

        if user_text in ["go to sleep", "sleep", "stop listening"]:
            speak("Okay, I am going to sleep.")
            active = False
            continue

        if open_command(user_text):
            continue

        # Time
        if "what time is it" in user_text or "current time" in user_text:
            current_time = datetime.now().strftime("%I:%M %p")
            speak(f"The current time is {current_time}.")
            continue

        # Date
        if "today" in user_text and "date" in user_text:
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today is {current_date}.")
            continue

        # Volume up
        if "volume up" in user_text:
            speak("Increasing volume.")
            for _ in range(5):
                ctypes.windll.user32.keybd_event(0xAF, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0xAF, 0, 2, 0)
            continue

        # Volume down
        if "volume down" in user_text:
            speak("Decreasing volume.")
            for _ in range(5):
                ctypes.windll.user32.keybd_event(0xAE, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0xAE, 0, 2, 0)
            continue

        # Mute
        if "mute" in user_text:
            speak("Muting volume.")
            ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0xAD, 0, 2, 0)
            continue

        # Screenshot
        if "take a screenshot" in user_text or "take screenshot" in user_text:
            screenshot = pyautogui.screenshot()
            filename = datetime.now().strftime("screenshot_%Y%m%d_%H%M%S.png")
            path = rf"C:\Users\abuba\Desktop\{filename}"
            screenshot.save(path)

            speak("Screenshot taken and saved on your desktop.")
            print(f"Screenshot saved: {path}")
            continue

        # Send everything else to AI
        response = ask_ai(user_text)

        print(f"AI: {response}")
        speak(response)


if __name__ == "__main__":
    main()