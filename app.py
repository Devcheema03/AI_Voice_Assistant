import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Voice Assistant")
st.write("Ask the AI anything.")

if "conversation" not in st.session_state:
    st.session_state.conversation = []

prompt = st.text_input("Enter your question:")

if st.button("Ask AI"):
    if prompt.strip():

        st.session_state.conversation.append(
            ("You", prompt)
        )

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
            if speaker == "You":
                messages.append({
                    "role": "user",
                    "content": message
                })
            else:
                messages.append({
                    "role": "assistant",
                    "content": message
                })

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            st.error("GROQ_API_KEY is not configured.")

        else:

            url = "https://api.groq.com/openai/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "llama-3.3-70b-versatile",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024
            }

            try:

                response = requests.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=60
                )

                if response.status_code == 200:

                    result = response.json()

                    answer = result["choices"][0]["message"]["content"]

                    st.session_state.conversation.append(
                        ("Assistant", answer)
                    )

                else:

                    st.error(
                        f"API Error: {response.status_code}"
                    )

                    st.code(response.text)

            except requests.exceptions.Timeout:

                st.error("The AI request timed out.")

            except requests.exceptions.RequestException as e:

                st.error(f"Connection error: {e}")

            except Exception as e:

                st.error(f"Unexpected error: {e}")


for speaker, message in st.session_state.conversation:

    if speaker == "You":

        st.markdown(
            f"**🧑 You:** {message}"
        )

    else:

        st.markdown(
            f"**🤖 Assistant:** {message}"
        )
