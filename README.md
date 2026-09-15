# 🤖 AI Voice Assistant

A Python-based AI Voice Assistant that allows users to interact with an AI using voice commands. The assistant captures speech through the microphone, converts speech to text, sends the request to an LLM, and converts the response back into speech.

## 🚀 Features

* 🎤 Speech-to-Text using SpeechRecognition
* 🧠 AI responses using an LLM
* 🔊 Text-to-Speech using pyttsx3
* 🖥️ Desktop GUI interface
* ⚙️ Environment variable configuration
* 🐍 Built with Python

## 🛠️ Technologies Used

* Python
* SpeechRecognition
* PyAudio
* pyttsx3
* Requests
* python-dotenv
* LLM API

## 📂 Project Structure

```text
AI_Voice_Assistant/
│
├── main.py
├── gui.py
├── Ilm.py
├── stt.py
├── tts.py
├── config.py
├── requirements.txt
└── Start_AI_Assistant.bat
```

## ⚙️ Installation

Clone the repository and install the required packages:

```bash
pip install -r requirements.txt
```

Configure your API settings in a `.env` file.

## ▶️ Run the Assistant

Run:

```bash
python main.py
```

Or use:

```text
Start_AI_Assistant.bat
```

## 🔐 Security

API keys and private credentials should be stored in `.env` and should never be uploaded to GitHub.

## 👨‍💻 Developer

**Abubakkar Cheema**

Computer Engineering Student | AI & Software Development
