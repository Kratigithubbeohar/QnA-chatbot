import ollama
import os
from dotenv import load_dotenv
load_dotenv()
client = ollama.Client()
response = client.chat(
    model="qwen2.5:3b",
    messages=[
        {"role": "user", "content": "what is the weather of hyderabad?"}
    ],
    options={"num_predict": 1000}
)
print(response.message.content)