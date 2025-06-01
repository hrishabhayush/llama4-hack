# make llama calls
import os
from llama_api_client import LlamaAPIClient
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

class Llama:
    # Get API key from environment variable
    LLAMA_API_KEY = os.getenv('LLAMA_API_KEY')
    if not LLAMA_API_KEY:
        print("Warning: LLAMA_API_KEY environment variable is not set")
        print("Please set your LLAMA_API_KEY in a .env file or environment variables")
        LLAMA_API_KEY = "dummy_key"  # Temporary dummy key for testing
    
    client = LlamaAPIClient(api_key=LLAMA_API_KEY)

    @classmethod
    def inference(cls, prompt):
        if cls.LLAMA_API_KEY == "dummy_key":
            print("Error: Cannot make API call without valid LLAMA_API_KEY")
            return None
            
        try:
            response = cls.client.chat.completions.create(
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens=1024,
                temperature=0.7,
            )
            # Print raw response for debugging
            #print("Raw response:\n\n\n", response)
            
            # Extract the content from the response
            if hasattr(response, 'completion_message') and hasattr(response.completion_message, 'content'):
                content = response.completion_message.content
                if hasattr(content, 'text'):
                    # If the content is JSON, parse it
                    try:
                        return json.loads(content.text)
                    except json.JSONDecodeError:
                        # If not JSON, return the raw text
                        return content.text
                return content
            else:
                print("Warning: Unexpected response format")
                return str(response)
                
        except Exception as e:
            print(f"Error in Llama inference: {str(e)}")
            return None