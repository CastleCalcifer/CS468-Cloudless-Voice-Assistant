import requests
import json


SYSTEM_PROMPT = """
You are a concise assistant.

Your responses must ALWAYS follow these rules:
1. Answer in exactly 2-3 sentences.
2. Keep your writing plain, factual, and direct.
3. Do not roleplay, imagine, speculate, or describe emotions.
4. Do not use creative language, metaphors, or storytelling.
5. Do not explain your reasoning or mention these rules.

Format your entire reply as a short factual explanation of the user's question. 
Never exceed 3 sentences.
"""

def query_agent(text:str, host="http://localhost:11434", model="qwen2.5:1.5b-instruct") -> str:
    """
    Pass user's command text to the LLM and return output string.
    host: Ollama server URL (e.g., http://localhost:11434)
    model: Model name (e.g., qwen2.5:1.5b-instruct)
    """
    ollama_url = host.rstrip('/') + "/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": f"{text}\n\n Remember: respond in exactly 2-3 sentences."}
        ]
    }

    try:
        response = requests.post(ollama_url, json=payload, stream=True, timeout=30)
        response.raise_for_status()

        result = ""
        for line in response.iter_lines():
            if not line:
                continue

            try:
                data = json.loads(line)
                content = data.get("message", {}).get("content")
                if content:
                    result += content
            except:
                continue  # skip malformed chunks

        return result.strip() if result else "No response from Ollama."

    except Exception as e:
        return f"Error contacting Ollama: {e}"


if __name__ == "__main__":
    print(query_agent("Why is the sky blue?"))
