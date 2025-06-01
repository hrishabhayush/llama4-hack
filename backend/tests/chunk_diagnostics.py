import sys
import os
import glob

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from ..utils.preprocessing import Preprocessor
from statistics import mean, median, stdev
from collections import Counter

def analyze_chunks(file_paths):
    preprocessor = Preprocessor()
    all_chunks = preprocessor.process_pdfs(file_paths)
    
    # Get sizes of all chunks
    chunk_sizes = [len(chunk['text']) for chunk in all_chunks]
    
    if not chunk_sizes:
        print("No chunks found!")
        return
    
    # Calculate statistics
    avg_size = mean(chunk_sizes)
    med_size = median(chunk_sizes)
    std_dev = stdev(chunk_sizes) if len(chunk_sizes) > 1 else 0
    
    # Create size distribution buckets (every 200 chars)
    buckets = Counter((size // 200) * 200 for size in chunk_sizes)
    
    print(f"\nChunk Size Analysis:")
    print(f"Total chunks: {len(chunk_sizes)}")
    print(f"Average size: {avg_size:.2f} characters")
    print(f"Median size: {med_size:.2f} characters")
    print(f"Standard deviation: {std_dev:.2f} characters")
    print(f"Min size: {min(chunk_sizes)} characters")
    print(f"Max size: {max(chunk_sizes)} characters")
    
    print("\nSize Distribution:")
    for size in sorted(buckets.keys()):
        print(f"{size}-{size+199}: {buckets[size]} chunks")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python chunk_diagnostics.py <pdf_directory>")
        print("The directory path should be relative to this script's location")
        sys.exit(1)
    
    # Get the directory path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_dir = os.path.join(script_dir, sys.argv[1])
    
    if not os.path.isdir(pdf_dir):
        print(f"Error: '{pdf_dir}' is not a valid directory!")
        sys.exit(1)
    
    # Find all PDF files in the directory
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in '{pdf_dir}'!")
        sys.exit(1)
    
    print(f"Found {len(pdf_files)} PDF files in {pdf_dir}")
    for pdf in pdf_files:
        print(f"- {os.path.basename(pdf)}")
    print("\nProcessing PDFs...")
    
    analyze_chunks(pdf_files) 