#Function declarations
import os
from backend.utils.preprocessing import Preprocessor
from backend.utils.Database import Chunk
from backend.utils.vectorize import create_vector_db, find_similar_idea_from_embedding
from backend.utils.LLMRequest import LLMRequest
from fastapi import FastAPI, UploadFile, File, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, Response
from backend.utils.env_checker import get_environment_config
from backend.utils.db_log import setup_logger
from backend.algo.core import cluster_ideas, get_cluster_summaries
from backend.utils.env_checker import check_environment
from backend.utils.env_checker import check_environment
from pydantic import BaseModel

# Initialize environment once at startup
check_environment()
ENV_CONFIG = get_environment_config()

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Or your frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],  # Add this line
    )

UPLOAD_DIR = "backend/files"

ENV_CONFIG = get_environment_config()
logger = setup_logger(__name__)

@app.get("/api/uploaded-files")
async def list_uploaded_files():
    files = []
    if os.path.exists(UPLOAD_DIR):
        files = [f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith('.pdf')]
    return JSONResponse(content={"files": files})

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"status": "success", "filename": file.filename}

# if user doesn't like the response, they can edit it
def edit_response():
    pass 

def generate(source_dir: str, prompt: str, debug: bool = os.getenv("DEBUG", "true").lower() == "true"):
    # Use the global environment config instead of checking again
    debug = ENV_CONFIG['debug_mode'] if debug is None else debug
    # process the pdfs
    preprocessor = Preprocessor()
    # create list of pdfs from the source_dir
    print (f"Source directory: {source_dir}")
    ___sources = os.listdir(source_dir)
    sources = []
    for source in ___sources:
        # Skip hidden files and non-PDF files
        if not source.startswith('.') and source.lower().endswith('.pdf'):
            sources.append(os.path.join(source_dir, source))

    print("Processing PDF files:", sources)
    print()
    pdf_texts = preprocessor.process_pdfs(sources)
    chunks = preprocessor.text_to_chunks(pdf_texts)

    # create a chunk object
    chunk_obj = Chunk(sources, "Quentin Kniep")
    ideas = []
    for chunk_dict in chunks:
        # Extend the ideas list with the list returned by chunk_to_idea
        ideas.extend(chunk_obj.chunk_to_idea(chunk_dict, debug=debug))
    
    # create a vector database
    client = create_vector_db(ideas)
    
    # Run k-means clustering on all ideas
    # nodes for the bubble map
    clusters, centroids = cluster_ideas(ideas, client)
    
    # Find similar ideas for each cluster centroid
    similar_ideas = []
    for centroid in centroids:
        cluster_similar_ideas = find_similar_idea_from_embedding(client, centroid.tolist(), limit=3)
        similar_ideas.extend(cluster_similar_ideas)

    # Print similar ideas and their quotations
    print("\nSimilar Ideas and Quotations:")
    for idea in similar_ideas:
        print(f"\nMain Point: {idea['main_point']}")
        quotation = chunk_obj.quotation.get(idea['quotation_id'], "Quotation not found")
        print(f"Quotation: {quotation}")
        print(f"Similarity Score: {idea['similarity_score']}")
    
    # Build bubble map nodes
    bubble_map_nodes = [
        {
            "id": str(idea["quotation_id"]),
            "label": idea["main_point"],
            "important": float(idea.get("similarity_score", 0)) > 0.8,
            "size": float(idea.get("similarity_score", 1)) * 20,
            "quotation": chunk_obj.quotation.get(idea["quotation_id"], "Quotation not found"),
            "similarity_score": idea.get("similarity_score", 0)
        }
        for idea in similar_ideas
    ]
    # For demo: connect all nodes in sequence (or you can use real similarity/cluster info)
    bubble_map_edges = []
    for i in range(len(bubble_map_nodes) - 1):
        bubble_map_edges.append({
            "source": bubble_map_nodes[i]["id"],
            "target": bubble_map_nodes[i+1]["id"],
            "weight": (bubble_map_nodes[i]["similarity_score"] + bubble_map_nodes[i+1]["similarity_score"]) / 2
        })
    bubble_map = {
        "nodes": bubble_map_nodes,
        "edges": bubble_map_edges
    }

    # Save bubble map to file for frontend access
    import json
    bubble_map_path = os.path.join(UPLOAD_DIR, "bubble-map.json")
    with open(bubble_map_path, "w") as f:
        json.dump(bubble_map, f)

    # format the response using Llama
    context = "\n".join([
        f"Main point: {idea['main_point']}\nQuotation: {chunk_obj.quotation.get(idea['quotation_id'], 'Quotation not found')}" 
        for idea in similar_ideas
    ])
    llama_prompt = f"""You are an expert research assistant. Using the following context from academic sources, provide a comprehensive answer to the user's question.

User's question: {prompt}

Relevant context from sources:
{context}

Please provide a detailed response that:
1. Directly addresses the user's question
2. Uses specific evidence from the provided quotations
3. Synthesizes the main points into a coherent argument in paragraphs, not bullet points
4. Maintains academic rigor and precision
5. Cite the sources for each direct quotation.
6. Use a wide range of sources to develop a nuanced and comprehensive answer.

Write your response as a well-structured paragraph that:
- Begins with a clear thesis statement
- Develops each main point with supporting evidence
- Uses smooth transitions between ideas
- Concludes with a synthesis of the key points
- Maintains a formal, academic tone throughout

Your response should be approximately 10 pages long."""

    # get response from Llama
    response = LLMRequest.inference(llama_prompt, debug=debug)
    logger.info(f"Response: {response}")
    return {"response": response, "bubble_map": bubble_map}

    
    # embeddings = vectorize(chunks)
    # store in vector database
    # query the vector database with the prompt
    # return the response

@app.get("/files/{filename}")
async def get_pdf(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Content-Disposition": f'inline; filename="{filename}"'
        }
        return FileResponse(file_path, media_type='application/pdf', headers=headers)
    return {"error": "File not found"}

@app.post("/api/generate")
async def generate_endpoint(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    source_dir = data.get("source_dir", "backend/files")
    response = generate(source_dir=source_dir, prompt=prompt)
    return {"response": response}

class OutlineContent(BaseModel):
    content: str

@app.post("/files/outline.txt")
async def save_outline_txt(data: OutlineContent):
    file_path = os.path.join(UPLOAD_DIR, "outline.txt")
    with open(file_path, "w") as f:
        f.write(data.content)
    return {"status": "success"}


