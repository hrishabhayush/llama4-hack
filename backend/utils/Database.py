#Class for an idea
import json
from .llama import Llama
import re

class Idea:
    def __init__(self, point, chunk_id, quotation_id):
        # implementation
        self.main_point = point
        self.chunk_id = chunk_id
        self.quotation_id = quotation_id

    def to_string(self):
        return f"Main Point: {self.main_point}, Chunk ID: {self.chunk_id}, Quotation ID: {self.quotation_id}"


class Chunk:
    # Class variable to track number of instances
    _instance_count = 0
    _point_instance_count = 0
    
    #inference for ideas for chunks too 
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.chunk_id = self.chunk_id_generator()
        self.quotation={}
    
    def chunk_id_generator(self):
        Chunk._instance_count += 1
        return Chunk._instance_count
    def quote_id_generator(self):
        Chunk._point_instance_count += 1
        return Chunk._point_instance_count
    
    def _clean_control_chars(self, text):
        """Clean invalid control characters from text before JSON parsing."""
        if not isinstance(text, str):
            return text
        # Remove all control characters except \n and \t
        return re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]', '', text)
    
    def chunk_to_idea(self,chunk):
        '''
        This function takes a json object with a "text" field, return a list of idea objects
        '''
        chunk_text= chunk["text"]
        prompt = f"""Imagine you are an expert in the field. Summarise the following text into 0 to 4 main points. Each point should be concise (1-3 sentences) and supported by a direct quotation.

Text to summarize:
{chunk_text}

Please format each "main point" as a JSON object:
{{
    "point": "First main point here",
    "quotation": "Supporting quotation from text"
}}

and return a JSON array of these objects.

Ensure each point is clear and each quotation directly supports its point.
Do not include any other text in your response outside of the JSON array.
Do not consider any references or citations."""
        
        response_data = Llama.inference(prompt)

        #print("Raw LLM Response: \n\n\n", response_data)  # Debug print
        
        # Parse the response and create Idea instances
        try:
            # Clean control characters and parse the JSON string into a list
            if isinstance(response_data, str):
                response_data = self._clean_control_chars(response_data)
                response_data = json.loads(response_data)
            
            ideas = []
            for point in response_data:
                idea = Idea(
                    point=point["point"],
                    chunk_id=self.chunk_id,
                    quotation_id=self.quote_id_generator()
                )
                ideas.append(idea)
                self.quotation[idea.quotation_id] = point["quotation"]
            #print("\n\n\nCreated Ideas:", [idea.to_string() for idea in ideas])  # Debug print
            return ideas
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)  # Debug print
            print("Failed character:", response_data[e.pos])  # Debug print
            print("Failed Response:", response_data)  # Debug print
            return []
        except Exception as e:
            print("Unexpected error:", e)  # Debug print
            print("Response data:", response_data)  # Debug print
            return []
    
    def to_string(self):
        return f"Title: {self.title}, Author: {self.author}, Chunk ID: {self.chunk_id}"