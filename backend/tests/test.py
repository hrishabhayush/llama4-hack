import os
import sys
import time
# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from backend.utils.preprocessing import Preprocessor
from backend.utils.Database import Chunk
from backend.api import generate
from backend.utils.LLMRequest import LLMRequest
def test_preprocessing():
    preprocessor = Preprocessor()
    pdf_texts = preprocessor.process_pdfs("Solana Alpenglow White Paper 2025-05-19.pdf")
    chunks = preprocessor.text_to_chunks(pdf_texts)
    print(chunks)

def test_chunk_to_idea():
    preprocessor = Preprocessor()
    pdf_texts = preprocessor.process_pdfs("Solana Alpenglow White Paper 2025-05-19.pdf")
    chunks = preprocessor.text_to_chunks(pdf_texts)
    chunk = Chunk("Solana Alpenglow White Paper 2025-05-19.pdf", "Quentin Kniep")
    ideas = chunk.chunk_to_idea(chunks[0])

    print(ideas)

def test_generate():
    start_time = time.time()
    result = generate("data/", "In recent years, U.S.–China relations have been characterized by increasing rivalry, strategic distrust, and competition over issues such as trade, technology, human rights, and regional security. Some analysts argue that this antagonism is driven by structural factors and an inevitable clash of interests, while others contend that cooperation remains possible and that pessimism about the relationship is overstated. Drawing on academic literature and recent policy developments, critically assess the main arguments on both sides of this debate. Should the U.S.–China relationship be viewed as an unavoidable zero-sum rivalry, or are there viable pathways for constructive engagement and mutual benefit? Support your analysis with specific examples, and consider the implications for global stability."
                      , debug=False)
    end_time = time.time()
    print("\n\n\n\n\nOutput:\n", result)
    print(f"Time taken: {end_time - start_time} seconds")

def test_llm():
    start_time = time.time()
    result = LLMRequest.inference("In recent years, U.S.–China relations have been characterized by increasing rivalry, strategic distrust, and competition over issues such as trade, technology, human rights, and regional security. Some analysts argue that this antagonism is driven by structural factors and an inevitable clash of interests, while others contend that cooperation remains possible and that pessimism about the relationship is overstated. Drawing on academic literature and recent policy developments, critically assess the main arguments on both sides of this debate. Should the U.S.–China relationship be viewed as an unavoidable zero-sum rivalry, or are there viable pathways for constructive engagement and mutual benefit? Support your analysis with specific examples, and consider the implications for global stability."
                                  , debug=True)
    end_time = time.time()
    print(result)
    print(f"Time taken: {end_time - start_time} seconds")

#Testing
#test_preprocessing()
if __name__ == "__main__":
    #test_chunk_to_idea()
    test_generate()
    #test_llm()