# core logic for ML algo
# k-means clustering
import numpy as np
from typing import List, Dict, Tuple
from ..utils.Database import Idea
from ..utils.vectorize import get_embedding, model
from qdrant_client import QdrantClient
from ..utils.db_log import setup_logger
import os
from tqdm import tqdm
from dotenv import load_dotenv

# Get logger for this module
load_dotenv()
logger = setup_logger(__name__)

def _kmeans_plus_plus_init(X: np.ndarray, k: int) -> np.ndarray:
    """
    Initialize cluster centers using k-means++ algorithm.
    
    Args:
        X: numpy array of shape (n_samples, n_features)
        k: number of clusters
    
    Returns:
        centroids: numpy array of shape (k, n_features)
    """
    n_samples, n_features = X.shape
    centroids = np.zeros((k, n_features))
    
    # Choose first centroid randomly
    first_centroid_idx = np.random.randint(n_samples)
    centroids[0] = X[first_centroid_idx]
    
    for i in range(1, k):
        distances = np.min([np.linalg.norm(X - centroid, axis=1)**2 
                          for centroid in centroids[:i]], axis=0)
        
        # Choose next centroid with probability proportional to distance squared
        probabilities = distances / distances.sum()
        next_centroid_idx = np.random.choice(n_samples, p=probabilities)
        centroids[i] = X[next_centroid_idx]
    
    return centroids

def cluster_ideas(ideas: List[Idea], client: QdrantClient = None) -> Tuple[Dict[int, List[Idea]], np.ndarray]:
    """
    Cluster ideas using k-means++ algorithm.
    
    Args:
        ideas: List of Idea objects to cluster
        client: QdrantClient instance (optional, not used for clustering but returned for convenience)
    
    Returns:
        clusters: Dictionary mapping cluster IDs to lists of Ideas
        centroids: Final centroid positions
    """
    # Get k from environment variable
    k = int(os.getenv('K_MEANS_CLUSTERS'))
    logger.info(f"Clustering {len(ideas)} ideas into {k} clusters")
    
    # Get embeddings for all ideas
    logger.info("Generating embeddings for clustering...")
    embeddings = []
    with tqdm(total=len(ideas), desc="Generating embeddings", unit="idea") as pbar:
        for idea in ideas:
            embedding = get_embedding(idea.main_point)
            embeddings.append(embedding)
            pbar.update(1)
    
    # Convert to numpy array
    X = np.array(embeddings)
    
    # Initialize centroids using k-means++
    logger.info("Initializing cluster centers with k-means++...")
    centroids = _kmeans_plus_plus_init(X, k)
    
    # K-means iteration
    max_iters = 100
    tolerance = 1e-4
    prev_centroids = None
    
    logger.info("Starting k-means iterations...")
    for iteration in tqdm(range(max_iters), desc="K-means iterations"):
        # Assign points to nearest centroid
        distances = np.array([np.linalg.norm(X - centroid, axis=1) 
                            for centroid in centroids])
        labels = np.argmin(distances, axis=0)
        
        # Update centroids
        prev_centroids = centroids.copy()
        for i in range(k):
            if np.sum(labels == i) > 0:  # Only update if cluster is not empty
                centroids[i] = np.mean(X[labels == i], axis=0)
        
        # Check convergence
        if prev_centroids is not None:
            diff = np.linalg.norm(centroids - prev_centroids)
            if diff < tolerance:
                logger.info(f"K-means converged after {iteration + 1} iterations")
                break
    
    # Create clusters dictionary
    clusters = {i: [] for i in range(k)}
    for idea, label in zip(ideas, labels):
        clusters[label].append(idea)
    
    # Log cluster sizes
    for cluster_id, cluster_ideas in clusters.items():
        logger.info(f"Cluster {cluster_id}: {len(cluster_ideas)} ideas")
    
    return clusters, centroids

def get_cluster_summaries(clusters: Dict[int, List[Idea]]) -> Dict[int, str]:
    """
    Get a summary of the main points in each cluster.
    
    Args:
        clusters: Dictionary mapping cluster IDs to lists of Ideas
    
    Returns:
        Dictionary mapping cluster IDs to summary strings
    """
    summaries = {}
    for cluster_id, ideas in clusters.items():
        main_points = [idea.main_point for idea in ideas]
        summary = f"Cluster {cluster_id} ({len(ideas)} ideas):\n"
        summary += "\n".join(f"- {point}" for point in main_points)
        summaries[cluster_id] = summary
    
    return summaries
