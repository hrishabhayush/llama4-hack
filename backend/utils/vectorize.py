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
from .db_log import setup_logger
from tqdm import tqdm
from backend.utils.env_checker import get_environment_config

# Get logger for this module
logger = setup_logger(__name__)

# Initialize the sentence transformer model
logger.info("Loading sentence transformer model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
logger.info("Model loaded successfully")

ENV_CONFIG = get_environment_config()

def get_qdrant_client():
    """
    Initialize Qdrant client based on environment
    Returns:
        client: QdrantClient instance
    """
    from backend.api import ENV_CONFIG
    
    if True:#ENV_CONFIG['debug_mode']:
        # Use local Qdrant instance in debug mode
        logger.info("Initializing local Qdrant instance (Debug mode)")
        client = QdrantClient(path="./qdrant_data")
    else:
        # Use production Qdrant instance
        logger.info(f"Connecting to Qdrant at {ENV_CONFIG['qdrant_url']}")
        client = QdrantClient(
            url=ENV_CONFIG['qdrant_url'],
            api_key=ENV_CONFIG['qdrant_api_key'] if ENV_CONFIG['qdrant_api_key'] else None
        )
    
    return client

def get_embedding(text: str) -> List[float]:
    """Convert text to embedding vector."""
    logger.debug(f"Generating embedding for text: {text[:50]}...")
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
    logger.info(f"Creating vector database with {len(sources)} ideas")
    
    # Initialize Qdrant client based on environment
    client = get_qdrant_client()
    
    # Create a new collection
    logger.info(f"Creating collection: {collection_name}")
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=model.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE
        )
    )
    
    # Prepare points for insertion
    logger.info("Generating embeddings for ideas...")
    points = []
    
    # Use tqdm to show progress of embedding generation
    for i, idea in enumerate(tqdm(sources, desc="Generating embeddings", unit="idea")):
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
    
    # Upload points in batches for better progress tracking
    batch_size = 100
    total_batches = (len(points) + batch_size - 1) // batch_size
    
    logger.info("Uploading points to Qdrant...")
    with tqdm(total=len(points), desc="Uploading to vector DB", unit="point") as pbar:
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            client.upsert(
                collection_name=collection_name,
                points=batch
            )
            pbar.update(len(batch))
    
    logger.info("Vector database creation completed successfully")
    return client

def find_similar_idea_from_embedding(client: QdrantClient, 
                               embedding: List[float], 
                               collection_name: str = "ideas", 
                               limit: int = 1) -> List[dict]:
    """
    Find the most similar ideas to a given embedding vector.
    
    Args:
        client: QdrantClient instance
        embedding: Pre-computed embedding vector
        collection_name: Name of the collection to search in
        limit: Number of results to return
        
    Returns:
        List of dictionaries containing the similar ideas and their metadata
    """
    logger.info("Searching for ideas similar to provided embedding...")
    
    # Search for similar vectors
    logger.debug(f"Querying collection '{collection_name}' for {limit} similar ideas")
    with tqdm(total=1, desc="Searching vector DB", leave=False) as pbar:
        search_result = client.search(
            collection_name=collection_name,
            query_vector=embedding,
            limit=limit
        )
        pbar.update(1)
    
    # Format results
    results = []
    for hit in search_result:
        results.append({
            "main_point": hit.payload["main_point"],
            "chunk_id": hit.payload["chunk_id"],
            "quotation_id": hit.payload["quotation_id"],
            "similarity_score": hit.score
        })
    
    logger.info(f"Found {len(results)} similar ideas")
    logger.debug(f"Search results: {results}")
    
    return results

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
    logger.info(f"Searching for ideas similar to: {prompt[:50]}...")
    
    # Get embedding for the prompt with progress indicator
    with tqdm(total=1, desc="Generating prompt embedding", leave=False) as pbar:
        prompt_embedding = get_embedding(prompt)
        pbar.update(1)
    
    # Use the embedding-based search function
    return find_similar_idea_from_embedding(
        client=client,
        embedding=prompt_embedding,
        collection_name=collection_name,
        limit=limit
    )
