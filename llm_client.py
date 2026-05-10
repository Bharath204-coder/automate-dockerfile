import requests

OLLAMA_BASE = "http://127.0.0.1:11434"

def generate_with_ollama(prompt: str, model: str = "codellama") -> str:
    print(f"  Sending to Ollama ({model})...")
    
    response = requests.post(
        f"{OLLAMA_BASE}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.15,
            },
        },
        timeout=600,
    )
    
    response.raise_for_status()
    return response.json()["response"].strip()


def generate_dockerfile_content(prompt: str) -> str:
    return generate_with_ollama(prompt)
