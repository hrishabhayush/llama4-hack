import os
import sys
# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, project_root)

from backend.utils.preprocessing import Preprocessor
from backend.utils.Database import Chunk
def test_preprocessing():
    preprocessor = Preprocessor()
    pdf_texts = preprocessor.process_pdfs("Solana Alpenglow White Paper 2025-05-19.pdf")
    chunks = preprocessor.text_to_chunks(pdf_texts)
    print(chunks)

def test_chunk_to_idea():
    chunk = Chunk("Solana Alpenglow White Paper 2025-05-19.pdf", "1")
    ideas = chunk.chunk_to_idea(chunk[0])
    print(ideas)

#Testing
#test_preprocessing()
test_chunk_to_idea()