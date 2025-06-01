import os
import sys
# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)

from backend.utils.preprocessing import Preprocessor
from backend.utils.Database import Chunk
from backend.api import generate

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
    return generate("Solana Alpenglow White Paper 2025-05-19.pdf", "What is the main idea of the white paper?")

#Testing
#test_preprocessing()
if __name__ == "__main__":
    #test_chunk_to_idea()
    test_generate()