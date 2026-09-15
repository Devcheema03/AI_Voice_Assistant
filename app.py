import streamlit as st
import requests
import os
import streamlit.components.v1 as components
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Voice Assistant")
st.write("Speak to your AI assistant.")

if "conversation" not in st.session_state:
    st.session_state.conversation = []


def speech_to_text(audio_file, api_key):

    url = "https://api.groq.com/openai/v1/audio/transcriptions"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    files = {
        "file": (
            "audio.wav",
            audio_file.getvalue(),
            "audio/wav"
        )
    }

    data = {
        "model": "whisper-large-v3-turbo",
        "language": "en",
        "response_format": "json"
    }

    response = requests.post(
        url,
        headers=headers,
        files=files,
        data=data,
        timeout=60
    )

    if response.status_code == 200:
        return response.json()["text"].strip()

    return None


def ask_ai(prompt, api_key):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI voice assistant. "
                "Give clear, simple and accurate answers."
            )
        }
    ]

    for speaker, message in st.session_state.conversation:
        messages.append({
            "role": "user" if speaker == "You" else "assistant",
            "content": message
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-oss-20b",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=60
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]

    return f"API Error: {response.status_code}"


def speak_answer(text):

    safe_text = (
        text.replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )

    html = f"""
    <script>
        const text = `{safe_text}`;

        const speech = new SpeechSynthesisUtterance(text);

        speech.lang = "en-US";
        speech.rate = 1.0;
        speech.pitch = 1.0;
        speech.volume = 1.0;

        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(speech);
    </script>
    """

    components.html(html, height=0)


api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is not configured.")
    st.stop()


st.subheader("🎤 Voice Input")

audio = st.audio_input(
    "Click the microphone and speak",
    sample_rate=16000
)

if audio:

    with st.spinner("🎧 Understanding your voice..."):

        try:

            spoken_text = speech_to_text(
                audio,
                api_key
            )

            if spoken_text:

                st.session_state.conversation.append(
                    ("You", spoken_text)
                )

                st.write(
                    f"**🧑 You said:** {spoken_text}"
                )

                with st.spinner("🤖 Thinking..."):

                    answer = ask_ai(
                        spoken_text,
                        api_key
                    )

                st.session_state.conversation.append(
                    ("Assistant", answer)
                )

                st.write(
                    f"**🤖 Assistant:** {answer}"
                )

                speak_answer(answer)

            else:

                st.error(
                    "I couldn't understand the audio."
                )

        except Exception as e:

            st.error(
                f"Voice error: {e}"
            )


st.divider()

st.subheader("⌨️ Text Input")

prompt = st.text_input(
    "Or type your question:"
)

if st.button("Ask AI") and prompt.strip():

    st.session_state.conversation.append(
        ("You", prompt)
    )

    with st.spinner("🤖 Thinking..."):

        answer = ask_ai(
            prompt,
            api_key
        )

    st.session_state.conversation.append(
        ("Assistant", answer)
    )

    st.write(
        f"**🤖 Assistant:** {answer}"
    )

    speak_answer(answer)


st.divider()

st.subheader("💬 Conversation")

for speaker, message in st.session_state.conversation:

    if speaker == "You":

        st.markdown(
            f"**🧑 You:** {message}"
        )

    else:

        st.markdown(
            f"**🤖 Assistant:** {message}"
        )
