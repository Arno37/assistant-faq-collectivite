from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("HF_TOKEN")
client = InferenceClient(token=token)

models_to_test = [
    "microsoft/Phi-3-mini-4k-instruct",
    "mistralai/Mistral-7B-Instruct-v0.3",
    "google/gemma-2-9b-it",
    "meta-llama/Llama-3.2-1B-Instruct"
]

for model in models_to_test:
    print(f"\n--- Testing {model} ---")
    try:
        response = client.chat_completion(
            model=model,
            messages=[{"role": "user", "content": "Bonjour, es-tu prêt ?"}],
            max_tokens=10
        )
        print(f"✅ Success: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ Error for {model}: {e}")
