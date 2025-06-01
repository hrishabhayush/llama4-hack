#Function declarations
import os
from backend.utils.preprocessing import Preprocessor
from backend.utils.Database import Chunk
from backend.utils.vectorize import create_vector_db, find_similar_idea
from backend.utils.LLMRequest import LLMRequest
from backend.utils.env_checker import check_environment, get_environment_config

# Initialize environment once at startup
check_environment()
ENV_CONFIG = get_environment_config()

# if user doesn't like the response, they can edit it
def edit_response():
    pass 

def generate(source_dir, prompt, debug=None):
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
    
    # find similar ideas to the prompt
    # TODO: we use k-means cluster to find 
    # "clouds" of ideas and present these as input to LLM
    similar_ideas = find_similar_idea(client, prompt, limit=3)
    
    # Create a mapping of ideas for easier lookup
    idea_map = {idea.quotation_id: idea for idea in ideas}
    
    # Print similar ideas and their quotations
    print("\nSimilar Ideas and Quotations:")
    formatted_ideas = []
    for similar_idea in similar_ideas:
        quotation_id = similar_idea.get('quotation_id')
        if quotation_id and quotation_id in chunk_obj.quotation:
            quotation = chunk_obj.quotation[quotation_id]
            print(f"\nMain Point: {similar_idea['main_point']}")
            print(f"Quotation: {quotation}")
            print(f"Similarity Score: {similar_idea['similarity_score']}")
            formatted_ideas.append({
                'main_point': similar_idea['main_point'],
                'quotation': quotation,
                'similarity_score': similar_idea['similarity_score']
            })
    
    # format the response using Llama
    context = "\n".join([
        f"Main point: {idea['main_point']}\nQuotation: {idea['quotation']}\nSimilarity Score: {idea['similarity_score']}" 
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


