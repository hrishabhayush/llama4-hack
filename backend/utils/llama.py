# make llama calls
import os
from llama_api_client import LlamaAPIClient

class Llama:
  # Get API key from environment variable
  LLAMA_API_KEY = os.getenv('LLAMA_API_KEY')
  if not LLAMA_API_KEY:
      raise ValueError("LLAMA_API_KEY environment variable is not set")
  client = LlamaAPIClient(api_key=LLAMA_API_KEY)

  def inference(prompt):
    response = client.chat.completions.create(
      model="Llama-4-Maverick-17B-128E-Instruct-FP8",
      messages=[
        {"role": "user", "content": prompt}
      ],
      max_completion_tokens=1024,
      temperature=0.7,
    )

    return response