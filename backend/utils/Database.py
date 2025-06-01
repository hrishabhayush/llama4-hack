#Class for an idea
import json
from .LLMRequest import LLMRequest
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
    
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.chunk_id = self.chunk_id_generator()
        self.quotation = {}
        # Use MAX_WORKERS_PER_CHUNK from environment variables
        self._max_workers = int(os.getenv('MAX_WORKERS_PER_CHUNK', '10'))
        # TODO: we should try to take in page numbers for better citations.
    
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
    
    def process_chunks_concurrently(self, chunks, debug=False):
        """
        Process multiple chunks concurrently using ThreadPoolExecutor
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed
        from tqdm import tqdm
        
        all_ideas = []
        
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            # Submit all chunks for processing
            future_to_chunk = {
                executor.submit(self._process_single_chunk, chunk, debug): chunk 
                for chunk in chunks
            }
            
            # Process completed futures as they come in
            for future in tqdm(as_completed(future_to_chunk), 
                             total=len(chunks),
                             desc="Processing chunks",
                             unit="chunk"):
                chunk = future_to_chunk[future]
                try:
                    ideas = future.result()
                    all_ideas.extend(ideas)
                except Exception as e:
                    print(f"Chunk processing failed: {str(e)}")
                    continue
                
        return all_ideas
    
    def _process_single_chunk(self, chunk, debug):
        """
        Process a single chunk and return its ideas
        """
        chunk_text = chunk["text"]
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
        
        response_data = LLMRequest.inference(prompt, debug=debug)
        
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
            return ideas
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON for chunk: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error processing chunk: {e}")
            return []
    
    def chunk_to_idea(self, chunk, debug=os.getenv("DEBUG").lower() == "true"):
        '''
        This function takes a json object with a "text" field, return a list of idea objects
        If multiple chunks are provided, processes them concurrently
        '''
        if isinstance(chunk, list):
            return self.process_chunks_concurrently(chunk, debug)
        else:
            return self._process_single_chunk(chunk, debug)
    
    def to_string(self):
        return f"Title: {self.title}, Author: {self.author}, Chunk ID: {self.chunk_id}"