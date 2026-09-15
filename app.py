import streamlit as st
import requests
import os
import streamlit.components.v1 as components
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #a0a0a0;
    font-size: 17px;
    margin-bottom: 20px;
}

.developer {
    text-align: center;
    color: #bbbbbb;
    font-size: 15px;
    margin-bottom: 20px;
}

.clock {
    text-align: center;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 25px;
}

.status {
    text-align: center;
    padding: 10px;
    border-radius: 10px;
    background-color: #17201b;
    border: 1px solid #285c3a;
    margin-bottom: 20px;
    font-weight: 600;
}

.user-message {
    background-color: #1c2733;
    padding: 14px;
    border-radius: 12px;
    margin: 10px 0;
}

.ai-message {
    background-color: #18251e;
    padding: 14px;
    border-radius: 12px;
    margin: 10px 0;
}

.feature-box {
    padding: 12px;
    border-radius: 10px;
    background-color: #161b22;
    margin-bottom: 8px;
}

.footer {
    text-align: center;
    color: #777777;
    font-size: 14px;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# SESSION STATE
# ==================================================

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="main-title">🤖 AI Voice Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your intelligent voice-powered AI assistant'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="developer">'
    '👨‍💻 Developed by <b>Abubakkar Cheema</b>'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# DATE & TIME
# ==================================================

current_time = datetime.now().strftime(
    "%A, %B %d, %Y | %I:%M:%S %p"
)

st.markdown(
    f'<div class="clock">🕐 {current_time}</div>',
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("⚙️ Assistant Settings")

    st.write("### 🎛️ Controls")

    if st.button(
        "🧹 Clear Conversation",
        use_container_width=True
    ):

        st.session_state.conversation = []

        st.rerun()


    if st.button(
        "🛑 Stop Speaking",
        use_container_width=True
    ):

        stop_html = """
        <script>
        window.speechSynthesis.cancel();
        </script>
        """

        components.html(
            stop_html,
            height=0
        )


    st.divider()

    st.write("### 🔊 Voice")

    voice_enabled = st.toggle(
        "Enable AI Voice",
        value=st.session_state.voice_enabled
    )

    st.session_state.voice_enabled = voice_enabled


    st.divider()

    st.write("### 📊 Project Information")

    st.markdown(
        """
        <div class="feature-box">
        🧠 <b>LLM</b><br>
        Groq GPT-OSS-20B
        </div>

        <div class="feature-box">
        🎤 <b>Speech Recognition</b><br>
        Whisper Large V3 Turbo
        </div>

        <div class="feature-box">
        🔊 <b>Text to Speech</b><br>
        Browser Speech API
        </div>

        <div class="feature-box">
        🌐 <b>Framework</b><br>
        Streamlit
        </div>

        <div class="feature-box">
        🐍 <b>Language</b><br>
        Python
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# API KEY
# ==================================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:

    st.error(
        "GROQ_API_KEY is not configured."
    )

    st.stop()


# ==================================================
# ASSISTANT STATUS
# ==================================================

st.markdown(
    '<div class="status">🟢 Assistant Ready</div>',
    unsafe_allow_html=True
)


# ==================================================
# SPEECH TO TEXT
# ==================================================

def speech_to_text(audio_file, api_key):

    url = (
        "https://api.groq.com/openai/v1/"
        "audio/transcriptions"
    )

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


# ==================================================
# AI / LLM
# ==================================================

def ask_ai(prompt, api_key):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a professional AI voice assistant. "
                "Give clear, useful, accurate and friendly "
                "answers. Keep answers reasonably concise "
                "unless the user asks for detail."
            )
        }
    ]

    for speaker, message in st.session_state.conversation:

        messages.append({
            "role": "user"
            if speaker == "You"
            else "assistant",
            "content": message
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    url = (
        "https://api.groq.com/openai/v1/"
        "chat/completions"
    )

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

        return (
            response.json()
            ["choices"][0]
            ["message"]["content"]
        )

    return f"API Error: {response.status_code}"


# ==================================================
# TEXT TO SPEECH
# ==================================================

def speak_answer(text):

    safe_text = (
        text
        .replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )

    html = f"""
    <script>

        const text = `{safe_text}`;

        const speech =
            new SpeechSynthesisUtterance(text);

        speech.lang = "en-US";
        speech.rate = 1.0;
        speech.pitch = 1.0;
        speech.volume = 1.0;

        window.speechSynthesis.cancel();

        window.speechSynthesis.speak(speech);

    </script>
    """

    components.html(
        html,
        height=0
    )


# ==================================================
# VOICE INPUT
# ==================================================

st.subheader("🎤 Voice Input")

audio = st.audio_input(
    "Click the microphone and speak",
    sample_rate=16000
)


if audio:

    with st.spinner(
        "🎧 Understanding your voice..."
    ):

        try:

            spoken_text = speech_to_text(
                audio,
                api_key
            )

            if spoken_text:

                st.session_state.conversation.append(
                    ("You", spoken_text)
                )

                st.markdown(
                    f"""
                    <div class="user-message">
                    🧑 <b>You:</b> {spoken_text}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                with st.spinner(
                    "🤖 Thinking..."
                ):

                    answer = ask_ai(
                        spoken_text,
                        api_key
                    )

                st.session_state.conversation.append(
                    ("Assistant", answer)
                )

                st.markdown(
                    f"""
                    <div class="ai-message">
                    🤖 <b>Assistant:</b><br>
                    {answer}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.session_state.voice_enabled:

                    speak_answer(answer)

            else:

                st.error(
                    "I couldn't understand the audio."
                )

        except Exception as e:

            st.error(
                f"Voice error: {e}"
            )


# ==================================================
# VOICE CONTROL BUTTONS
# ==================================================

st.divider()

st.subheader("🎛️ Voice Controls")

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "🛑 Stop Speaking",
        use_container_width=True
    ):

        stop_html = """
        <script>
        window.speechSynthesis.cancel();
        </script>
        """

        components.html(
            stop_html,
            height=0
        )


with col2:

    if st.button(
        "🎤 Ask Another Question",
        use_container_width=True
    ):

        stop_html = """
        <script>
        window.speechSynthesis.cancel();
        </script>
        """

        components.html(
            stop_html,
            height=0
        )

        st.rerun()


with col3:

    if st.button(
        "🧹 Clear Chat",
        use_container_width=True
    ):

        st.session_state.conversation = []

        st.rerun()


# ==================================================
# TEXT INPUT
# ==================================================

st.divider()

st.subheader("⌨️ Text Input")

prompt = st.text_input(
    "Type your question here:",
    placeholder="Ask anything..."
)

if prompt:

    st.caption(
        f"{len(prompt)} characters"
    )


if st.button(
    "🚀 Ask AI",
    use_container_width=True
) and prompt.strip():

    st.session_state.conversation.append(
        ("You", prompt)
    )

    with st.spinner(
        "🤖 Thinking..."
    ):

        answer = ask_ai(
            prompt,
            api_key
        )

    st.session_state.conversation.append(
        ("Assistant", answer)
    )

    st.markdown(
        f"""
        <div class="user-message">
        🧑 <b>You:</b> {prompt}
        </div>

        <div class="ai-message">
        🤖 <b>Assistant:</b><br>
        {answer}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.voice_enabled:

        speak_answer(answer)


# ==================================================
# CONVERSATION HISTORY
# ==================================================

st.divider()

st.subheader("💬 Conversation History")

if not st.session_state.conversation:

    st.info(
        "No conversation yet. "
        "Use the microphone or type a question."
    )

else:

    for speaker, message in (
        st.session_state.conversation
    ):

        if speaker == "You":

            st.markdown(
                f"""
                <div class="user-message">
                🧑 <b>You:</b> {message}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="ai-message">
                🤖 <b>Assistant:</b><br>
                {message}
                </div>
                """,
                unsafe_allow_html=True
            )


# ==================================================
# DOWNLOAD CONVERSATION
# ==================================================

if st.session_state.conversation:

    conversation_text = ""

    for speaker, message in (
        st.session_state.conversation
    ):

        conversation_text += (
            f"{speaker}: {message}\n\n"
        )

    st.download_button(
        "📥 Download Conversation",
        data=conversation_text,
        file_name="AI_Assistant_Conversation.txt",
        mime="text/plain",
        use_container_width=True
    )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.markdown(
    """
    <div class="footer">
    🤖 AI Voice Assistant<br>
    Developed by <b>Abubakkar Cheema</b><br>
    Python • Streamlit • Groq • Whisper • LLM
    </div>
    """,
    unsafe_allow_html=True
)
