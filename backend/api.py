#Function declarations
import os
from backend.utils.preprocessing import Preprocessor
from backend.utils.Database import Chunk
from backend.utils.vectorize import create_vector_db, find_similar_idea
from backend.utils.llama import Llama

# if user doesn't like the response, they can edit it
def edit_response():
    pass 

def generate(sources, prompt):
    # process the pdfs
    preprocessor = Preprocessor()
    pdf_texts = preprocessor.process_pdfs(sources)
    chunks = preprocessor.text_to_chunks(pdf_texts)

    # create a chunk object
    chunk = Chunk(sources, "Quentin Kniep")
    ideas = []
    for chunk in chunks:
        # Extend the ideas list with the list returned by chunk_to_idea
        ideas.extend(chunk.chunk_to_idea(chunk))
    
    # create a vector database
    client = create_vector_db(ideas)
    
    # find similar ideas to the prompt
    similar_ideas = find_similar_idea(client, prompt, limit=3)
    
    # match quotation with ideas
    for idea in ideas:
        for similar_idea in similar_ideas:
            if idea.quotation_id == similar_idea['quotation_id']:
                similar_idea['quotation'] = chunk.quotation[idea.quotation_id]
    
    # format the response using Llama
    context = "\n".join([f"Main point: {idea['main_point']}\nQuotation: {idea['quotation']}" for idea in similar_ideas])
    llama_prompt = f"""Based on the following context, provide a comprehensive response to: {prompt}

Context:
{context}"""

    return response

    
    # embeddings = vectorize(chunks)
    # store in vector database
    # query the vector database with the prompt
    # return the response
    pass


