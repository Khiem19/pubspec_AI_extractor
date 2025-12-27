import os
import requests

def llm_chat(prompt: str) -> str:
    """
    Calls llama.cpp server (OpenAI-compatible endpoint) running in Docker.
    Expects the server at LLM_BASE_URL, e.g. http://llm:8080
    """
    base = os.environ.get("LLM_BASE_URL", "http://localhost:8080").rstrip("/")
    url = f"{base}/v1/chat/completions"

    payload = {
        "model": "local-gguf",
        "messages": [
            {"role": "system", "content": "Return JSON only. No markdown. No explanations."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.0,
    }

    r = requests.post(url, json=payload, timeout=600)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"].strip()
