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

        history = "\n".join(
            f"{speaker}: {message}"
            for speaker, message in st.session_state.conversation
        )

        full_prompt = f"""
You are a helpful AI assistant.

Conversation:
{history}

Assistant:
"""

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
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                "temperature": 0.7
            }

            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=60
                )

                if response.status_code == 200:
                    answer = response.json()["choices"][0]["message"]["content"]

                    st.session_state.conversation.append(
                        ("Assistant", answer)
                    )

                else:
                    st.error(
                        f"API Error: {response.status_code}"
                    )

            except Exception as e:
                st.error(f"Error: {e}")

for speaker, message in st.session_state.conversation:
    if speaker == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Assistant:** {message}")
