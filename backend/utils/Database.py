#Class for an idea
from llama import Llama
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
    
    def chunk_to_idea(self, json):
        '''
        This function takes a json object with a "text" field, return a list of idea objects
        '''
        chunk_text = json["text"]
        prompt = f"""Summarise the following text into 2 main points. Each point should be concise (1-3 sentences) and supported by a direct quotation.

Text to summarize:
{chunk_text}

Please format your response exactly like this:
{{
    "main_points": [
        {{
            "point": "First main point here",
            "quotation": "Supporting quotation from text"
        }},
        {{
            "point": "Second main point here",
            "quotation": "Supporting quotation from text"
        }}
    ]
}}

Ensure each point is clear and each quotation directly supports its point."""
        
        response = Llama.inference(prompt)
        
        print("Raw LLM Response:", response)  # Debug print
        
        # Parse the response and create Idea instances
        try:
            response_data=response.json()["completion_message"]["content"]["text"]
            print("Parsed Response Data:", response_data)  # Debug print
            ideas = []
            for point in response_data["main_points"]:
                idea = Idea(
                    point=point["point"],
                    chunk_id=self.chunk_id,
                    quotation_id=self.quote_id_generator()
                )
                ideas.append(idea)
                self.quotation[idea.quotation_id] = point["quotation"]
            print("Created Ideas:", [idea.to_string() for idea in ideas])  # Debug print
            return ideas
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)  # Debug print
            print("Failed Response:", response)  # Debug print
            return []
    
    def to_string(self):
        return f"Title: {self.title}, Author: {self.author}, Chunk ID: {self.chunk_id}"