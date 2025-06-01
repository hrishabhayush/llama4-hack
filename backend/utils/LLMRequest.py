# make llama calls
import os
from dotenv import load_dotenv
import json


# Load environment variables from .env file
load_dotenv()


class LLMRequest:
    client = None

    @classmethod
    def initialize_client(cls):
        cls.__LLM_MODEL = os.getenv("LLM").lower()
        if cls.__LLM_MODEL == "llama":
            from llama_api_client import LlamaAPIClient
        elif cls.__LLM_MODEL == "cerebras":
            from cerebras.cloud.sdk import Cerebras
        else:
            raise ValueError("Invalid LLM model")

        api_key = os.environ.get("API_KEY")
        if cls.__LLM_MODEL == "llama":
            cls.client = LlamaAPIClient(api_key=api_key)
        elif cls.__LLM_MODEL == "cerebras":
            cls.client = Cerebras(api_key=api_key)

    @classmethod
    def inference(cls, prompt, debug=os.getenv("DEBUG").lower() == "true"):
        if cls.client is None:
            cls.initialize_client()
        try:
            # Extract the content from the response
            if cls.__LLM_MODEL == "llama":
                response = cls.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                            "response_format": {
                                "type": "json_schema",
                                "json_schema": {
                                    "schema": {
                                        "type": "object"
                                    }
                                }
                            }
                        }
                    ],
                    model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                    
                )
                # Print raw response for debugging
                if debug:
                    print("Raw response:\n\n\n", response)

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
            elif cls.__LLM_MODEL == "cerebras":
                response = cls.client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                ],
                    model="llama-4-scout-17b-16e-instruct",
                )
                # Print raw response for debugging
                if debug:
                    print("Raw response:\n\n\n", response)

                if (hasattr(response, 'choices') and len(response.choices) > 0 
                        and hasattr(response.choices[0], 'message') 
                        and hasattr(response.choices[0].message, 'content')):
                    content = response.choices[0].message.content
                    return content
                else:
                    print("Warning: Unexpected response format")
                    return str(response)
        except Exception as e:
            print(f"Error in inference: {str(e)}")
            return None