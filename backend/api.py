#Function declarations
import os
from backend.utils.preprocessing import Preprocessor
from backend.utils.Database import Chunk
from backend.utils.vectorize import create_vector_db, find_similar_idea_from_embedding
from backend.utils.LLMRequest import LLMRequest
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, Response
from backend.algo.core import cluster_ideas, get_cluster_summaries

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

@app.post("/api/generate")
def generate(source_dir: str, prompt: str, debug = None):
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
    
    # Process all chunks concurrently
    print("\nProcessing chunks with concurrent LLM inference...")
    ideas = chunk_obj.chunk_to_idea(chunks, debug=debug)
    
    # create a vector database
    client = create_vector_db(ideas)
    
    # Run k-means clustering on all ideas
    clusters, centroids = cluster_ideas(ideas)
    
    # Find similar ideas for each cluster centroid
    similar_ideas = []
    for centroid in centroids:
        cluster_similar_ideas = find_similar_idea_from_embedding(client, centroid.tolist(), limit=3)
        similar_ideas.extend(cluster_similar_ideas)
    
    # Print similar ideas and their quotations
    print("\nSimilar Ideas and Quotations:")
    formatted_ideas = []
    for similar_idea in similar_ideas:
        quotation_id = similar_idea.get('quotation_id')
        chunk_id = similar_idea.get('chunk_id')
        
        # Get the source information based on chunk_id
        source_index = chunk_id - 1  # Since chunk_id starts from 1
        source_title = sources[source_index] if 0 <= source_index < len(sources) else "Unknown"
        
        if quotation_id and quotation_id in chunk_obj.quotation:
            quotation = chunk_obj.quotation[quotation_id]
            print(f"\nMain Point: {similar_idea['main_point']}")
            print(f"Quotation: {quotation}")
            print(f"Source: {source_title}")
            print(f"Author: {chunk_obj.author}")
            print(f"Similarity Score: {similar_idea['similarity_score']}")
            formatted_ideas.append({
                'main_point': similar_idea['main_point'],
                'quotation': quotation,
                'title': source_title,
                'author': chunk_obj.author,
                'chunk_id': chunk_id
            })
    
    # format the response using Llama
    context = "\n".join([
        f"Main point: {idea['main_point']}\nQuotation: {idea['quotation']}\nSource: {idea['title']}\nAuthor: {idea['author']}" 
        for idea in formatted_ideas
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
    
    return response

    
    # embeddings = vectorize(chunks)
    # store in vector database
    # query the vector database with the prompt
    # return the response
    pass

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


