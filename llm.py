import requests


conversation = []


def ask_ai(prompt):
    conversation.append(f"User: {prompt}")

    history = "\n".join(conversation)

    full_prompt = f"""
You are a helpful AI voice assistant.
Use the conversation history to understand previous messages.

Conversation:
{history}

Assistant:
"""

    url = "http://localhost:11434/api/generate"

    data = {
        "model": "llama3.2:3b",
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=data, timeout=60)

        if response.status_code == 200:
            answer = response.json()["response"].strip()
            conversation.append(f"Assistant: {answer}")
            return answer

        return f"Ollama Error: {response.status_code}"

    except requests.exceptions.ConnectionError:
        return "I cannot connect to Ollama. Please make sure Ollama is running."

    except requests.exceptions.Timeout:
        return "The AI took too long to respond."

    except Exception as e:
        return f"An unexpected error occurred: {e}"


if __name__ == "__main__":
    print(ask_ai("My name is Abubakkar."))
    print(ask_ai("What is my name?"))