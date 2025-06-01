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
    chunk_obj = Chunk(sources, "Quentin Kniep")
    ideas = []
    for chunk_dict in chunks:
        # Extend the ideas list with the list returned by chunk_to_idea
        ideas.extend(chunk_obj.chunk_to_idea(chunk_dict))
    
    # create a vector database
    client = create_vector_db(ideas)
    
    # find similar ideas to the prompt
    similar_ideas = find_similar_idea(client, prompt, limit=3)
    
    # match quotation with ideas
    for idea in ideas:
        for similar_idea in similar_ideas:
            if idea.quotation_id == similar_idea['quotation_id']:
                similar_idea['quotation'] = chunk_obj.quotation[idea.quotation_id]
    
    # Print similar ideas and their quotations
    print("\nSimilar Ideas and Quotations:")
    for idea in similar_ideas:
        print(f"\nMain Point: {idea['main_point']}")
        print(f"Quotation: {idea['quotation']}")
        print(f"Similarity Score: {idea['similarity_score']}")
    
    # format the response using Llama
    context = "\n".join([f"Main point: {idea['main_point']}\nQuotation: {idea['quotation']}" for idea in similar_ideas])
    llama_prompt = f"""You are an expert research assistant. Using the following context from academic sources, provide a comprehensive answer to the user's question.

User's question: {prompt}

Relevant context from sources:
{context}

Please provide a detailed response that:
1. Directly addresses the user's question
2. Uses specific evidence from the provided quotations
3. Synthesizes the main points into a coherent argument
4. Maintains academic rigor and precision

Write your response as a well-structured paragraph that:
- Begins with a clear thesis statement
- Develops each main point with supporting evidence
- Uses smooth transitions between ideas
- Concludes with a synthesis of the key points
- Maintains a formal, academic tone throughout

Your response should be approximately 1-2 paragraphs long."""

    # get response from Llama
    response = Llama.inference(llama_prompt)
    
    return response

    
    # embeddings = vectorize(chunks)
    # store in vector database
    # query the vector database with the prompt
    # return the response
    pass


