# vectorize.py
# We vectorize Ideas into embeddings and store them in a vector database
# Sentence Transformers is used to vectorize the Ideas
# Qdrant is used to store the embeddings
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams
import os
from sentence_transformers import SentenceTransformer
from typing import List
from .Database import Idea
from .env_checker import check_environment, EnvironmentError

# Check environment variables before proceeding
check_environment()

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_qdrant_client():
    """
    Initialize Qdrant client based on environment
    Returns:
        client: QdrantClient instance
    """
    debug_mode = os.getenv('DEBUG', 'True').lower() == 'true'
    
    if debug_mode:
        # Use local Qdrant instance in debug mode
        client = QdrantClient(path="./qdrant_data")
        print("Using local Qdrant instance (Debug mode)")
    else:
        # Use production Qdrant instance
        qdrant_url = os.getenv('QDRANT_URL')
        qdrant_api_key = os.getenv('QDRANT_API_KEY')
        
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key if qdrant_api_key else None
        )
        print(f"Connected to Qdrant at {qdrant_url}")
    
    return client

def get_embedding(text: str) -> List[float]:
    """Convert text to embedding vector."""
    return model.encode(text).tolist()

def create_vector_db(sources: List[Idea], collection_name: str = "ideas") -> QdrantClient:
    """
    Create a vector database from a list of Idea objects.
    
    Args:
        sources: List of Idea objects
        collection_name: Name of the collection to create
        
    Returns:
        QdrantClient instance
    """
    # Initialize Qdrant client based on environment
    client = get_qdrant_client()
    
    # Create a new collection
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=model.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE
        )
    )
    
    # Prepare points for insertion
    points = []
    for i, idea in enumerate(sources):
        embedding = get_embedding(idea.main_point)
        
        points.append(models.PointStruct(
            id=i,
            vector=embedding,
            payload={
                "main_point": idea.main_point,
                "chunk_id": idea.chunk_id,
                "quotation_id": idea.quotation_id
            }
        ))
    
    # Upload points in batches
    client.upsert(
        collection_name=collection_name,
        points=points
    )
    
    return client

def find_similar_idea(client: QdrantClient, prompt: str, collection_name: str = "ideas", limit: int = 1) -> List[dict]:
    """
    Find the most similar ideas to a given prompt.
    
    Args:
        client: QdrantClient instance
        prompt: Text prompt to search for
        collection_name: Name of the collection to search in
        limit: Number of results to return
        
    Returns:
        List of dictionaries containing the similar ideas and their metadata
    """
    # Get embedding for the prompt
    prompt_embedding = get_embedding(prompt)
    
    # Search for similar vectors
    search_result = client.search(
        collection_name=collection_name,
        query_vector=prompt_embedding,
        limit=limit
    )
    
    # Format results
    results = []
    for hit in search_result:
        results.append({
            "main_point": hit.payload["main_point"],
            "chunk_id": hit.payload["chunk_id"],
            "quotation_id": hit.payload["quotation_id"],
            "similarity_score": hit.score
        })
    
    return results
