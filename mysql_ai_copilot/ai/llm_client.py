import urllib.request
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def chat(messages):
    prompt = messages[-1]["content"]

    data = {
        "model": "qwen3:8b",
        "prompt": prompt,
        "stream": False
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=6000) as response:
        result = json.loads(response.read().decode("utf-8"))
        return result["response"]
