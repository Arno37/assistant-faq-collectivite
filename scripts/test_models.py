from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("HF_TOKEN")
client = InferenceClient(token=token)

# Liste élargie pour trouver un survivant stable
models_to_test = [
    "meta-llama/Llama-3.1-8B-Instruct",
    "meta-llama/Llama-3.2-3B-Instruct",
    "Qwen/Qwen2.5-7B-Instruct",
    "meta-llama/Llama-2-7b-chat-hf",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "google/gemma-2-9b-it"
]

print(f"--- Diagnostic des modèles (Token: {token[:5]}...) ---")

for model in models_to_test:
    print(f"\n🔍 Test de {model}...")
    try:
        response = client.chat_completion(
            model=model,
            messages=[{"role": "user", "content": "Bonjour, réponds 'OK'."}],
            max_tokens=5
        )
        print(f"✅ SUCCÈS : {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ ÉCHEC : {str(e)[:100]}")
