# return list of strings
from PyPDF2 import PdfReader
import re
from typing import List, Dict, Optional
from multiprocessing import Pool, cpu_count
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import partial
import os
import torch
import logging
from enum import Enum
from dataclasses import dataclass
from .db_log import setup_logger
from tqdm import tqdm
from dotenv import load_dotenv
# Get logger for this module
load_dotenv()
logger = setup_logger(__name__)

class Environment(Enum):
    DEBUG = "debug"
    PRODUCTION = "production"

@dataclass
class ResourceConfig:
    env_type: Environment
    num_gpus: int
    num_cpus: int
    memory_limit: Optional[int] = None
    gpu_memory_limits: Optional[List[int]] = None

class Preprocessor:
    def __init__(self):
        """Initialize the preprocessor with environment-aware configuration"""
        # Initialize logging
        self.logger = logger
        
        # Define chunking parameters from environment variables
        print(f"Reading MIN_CHUNK from env: {os.getenv('MIN_CHUNK_SIZE')}")
        print(f"Reading MAX_CHUNK from env: {os.getenv('MAX_CHUNK_SIZE')}")
        
        self.min_chunk_size = int(os.getenv('MIN_CHUNK_SIZE'))
        self.max_chunk_size = int(os.getenv('MAX_CHUNK_SIZE'))
        
        # Define section break patterns
        self.section_breaks = [
            r'\n\s*\n',  # Double newlines
            r'\.\s+(?=[A-Z])',  # Period followed by capital letter
            r'[!?]\s+',  # Exclamation or question mark
            r'\n(?=\d+\.\s)',  # Numbered lists
            r'\n(?=[A-Z]\.\s)',  # Lettered lists
            r'\n(?=•|\-|\*)',  # Bullet points
        ]
        
        # Define semantic markers
        self.semantic_markers = [
            r'First,|Second,|Third,|Finally,',
            r'In conclusion,|To summarize,|In summary,',
            r'However,|Moreover,|Furthermore,|Additionally,',
            r'For example,|Specifically,|In particular,',
            r'On the other hand,|In contrast,',
            r'Therefore,|Thus,|Hence,',
        ]
        
        # Initialize resource configuration
        self.resource_config = self._initialize_resources()
        self.logger.info(f"Initialized with resource config: {self.resource_config}")
        
        # Initialize device configuration
        self.devices = self._initialize_devices()

    def _initialize_resources(self) -> ResourceConfig:
        """
        Initialize resource configuration based on environment
        """
        from backend.api import ENV_CONFIG
        
        env_type = Environment.DEBUG if ENV_CONFIG['debug_mode'] else Environment.PRODUCTION
        
        if env_type == Environment.PRODUCTION:
            # In production, detect available GPUs
            num_gpus = torch.cuda.device_count() if torch.cuda.is_available() else 0
            num_cpus = cpu_count()
            
            # Get GPU memory limits if available
            gpu_memory_limits = None
            if num_gpus > 0:
                gpu_memory_limits = [
                    torch.cuda.get_device_properties(i).total_memory 
                    for i in range(num_gpus)
                ]
            
            return ResourceConfig(
                env_type=env_type,
                num_gpus=num_gpus,
                num_cpus=num_cpus,
                memory_limit=ENV_CONFIG['memory_limit_gb'],
                gpu_memory_limits=gpu_memory_limits
            )
        else:
            # Debug mode - use minimal resources
            return ResourceConfig(
                env_type=env_type,
                num_gpus=0,
                num_cpus=min(4, cpu_count()),  # Limit CPU usage in debug
                memory_limit=None
            )

    def _initialize_devices(self) -> List[str]:
        """
        Initialize available devices for processing
        """
        devices = []
        
        if self.resource_config.env_type == Environment.PRODUCTION:
            # In production, try to use GPUs first
            if self.resource_config.num_gpus > 0:
                for i in range(self.resource_config.num_gpus):
                    devices.append(f'cuda:{i}')
            
            # Always add CPU as fallback
            devices.append('cpu')
        else:
            # In debug, just use CPU
            devices.append('cpu')
        
        return devices

    def _get_optimal_batch_size(self, text_length: int) -> int:
        """
        Calculate optimal batch size based on available resources
        """
        if self.resource_config.env_type == Environment.DEBUG:
            return 1
        
        # Base batch size on available memory and text length
        if self.resource_config.memory_limit:
            # Rough estimate: each character takes 2 bytes
            estimated_text_memory = text_length * 2
            return max(1, self.resource_config.memory_limit // estimated_text_memory)
        
        # Default batch sizes
        return 32 if self.resource_config.num_gpus > 0 else 16

    def process_pdfs(self, sources):
        """Process PDFs using environment-appropriate resources"""
        self.logger.info(f"Processing {len(sources)} PDFs...")
        
        # Determine optimal number of workers
        if self.resource_config.env_type == Environment.PRODUCTION:
            num_threads = min(len(sources), self.resource_config.num_cpus * 4, 32)
        else:
            num_threads = min(len(sources), 4)  # Limited threads in debug mode
        
        # First, use threads to read PDFs (I/O-bound)
        with ThreadPoolExecutor(max_workers=num_threads) as thread_pool:
            # Use tqdm to show progress of PDF processing
            pdf_contents = list(tqdm(
                thread_pool.map(self.process_1_pdf, sources),
                total=len(sources),
                desc="Processing PDFs",
                unit="pdf"
            ))
        
        # Flatten and prepare for processing
        text_with_sources = []
        for source_idx, pages in enumerate(pdf_contents):
            for page_idx, text in enumerate(pages):
                if text.strip():
                    text_with_sources.append({
                        'text': text,
                        'source': sources[source_idx],
                        'page': page_idx
                    })
        
        if not text_with_sources:
            return []
        
        # Determine batch size based on available resources
        batch_size = self._get_optimal_batch_size(
            sum(len(t['text']) for t in text_with_sources)
        )
        
        # Process in batches using available resources
        if self.resource_config.env_type == Environment.PRODUCTION and self.resource_config.num_gpus > 0:
            return self._process_with_gpu(text_with_sources, batch_size)
        else:
            return self._process_with_cpu(text_with_sources)

    def _process_with_gpu(self, text_with_sources: List[Dict], batch_size: int) -> List[Dict]:
        """Process texts using available GPUs"""
        self.logger.info(f"Processing with {self.resource_config.num_gpus} GPUs, batch size {batch_size}")
        
        # Split work across available GPUs
        chunks_per_gpu = len(text_with_sources) // self.resource_config.num_gpus
        all_chunks = []
        
        with ProcessPoolExecutor(max_workers=self.resource_config.num_gpus) as executor:
            futures = []
            
            # Create progress bar for GPU processing
            with tqdm(total=len(text_with_sources), desc="GPU Processing", unit="text") as pbar:
                for gpu_idx in range(self.resource_config.num_gpus):
                    start_idx = gpu_idx * chunks_per_gpu
                    end_idx = start_idx + chunks_per_gpu if gpu_idx < self.resource_config.num_gpus - 1 else len(text_with_sources)
                    
                    if start_idx < end_idx:
                        future = executor.submit(
                            self._process_batch_gpu,
                            text_with_sources[start_idx:end_idx],
                            f'cuda:{gpu_idx}',
                            batch_size,
                            end_idx - start_idx  # Pass chunk size for progress tracking
                        )
                        futures.append(future)
                
                # Collect results and update progress
                for future in futures:
                    chunks = future.result()
                    all_chunks.extend(chunks)
                    pbar.update(chunks_per_gpu)
        
        return all_chunks

    def _process_batch_gpu(self, texts: List[Dict], device: str, batch_size: int, chunk_size: int) -> List[Dict]:
        """
        Process a batch of texts on a specific GPU
        """
        chunks = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_chunks = [self._process_single_text(text) for text in batch]
            chunks.extend([c for sublist in batch_chunks for c in sublist])
        return chunks

    def _process_with_cpu(self, text_with_sources: List[Dict]) -> List[Dict]:
        """Process texts using CPU resources"""
        num_workers = self.resource_config.num_cpus
        if self.resource_config.env_type == Environment.DEBUG:
            num_workers = min(num_workers, 4)
        
        self.logger.info(f"Processing with {num_workers} CPU workers")
        
        with ProcessPoolExecutor(max_workers=num_workers) as pool:
            # Use tqdm to show progress of CPU processing
            chunk_lists = list(tqdm(
                pool.map(self._process_single_text, text_with_sources),
                total=len(text_with_sources),
                desc="Processing texts",
                unit="text"
            ))
        
        return [chunk for sublist in chunk_lists for chunk in sublist]

    def process_1_pdf(self, source):
        """Process a single PDF - this is I/O bound so we use it with ThreadPoolExecutor"""
        text = []
        try:
            reader = PdfReader(source)
            # Extract text from all pages
            for page in tqdm(
                reader.pages,
                desc=f"Extracting text from {os.path.basename(source)}",
                leave=False,
                unit="page"
            ):
                text.append(page.extract_text())
        except Exception as e:
            self.logger.error(f"Error processing PDF {source}: {str(e)}")
        return text

    def _process_single_text(self, text_info: dict) -> List[Dict]:
        """
        Process a single text into chunks - CPU bound operation
        
        Args:
            text_info: Dictionary containing text and metadata
                {
                    'text': str,
                    'source': str,
                    'page': int
                }
        Returns:
            List of chunk dictionaries
        """
        # Extract text and metadata from input
        if isinstance(text_info, dict):
            text = text_info.get('text', '')
            source = text_info.get('source', 'unknown')
            page_num = text_info.get('page', 0)
        else:
            # Handle legacy string input for backward compatibility
            text = str(text_info)
            source = 'unknown'
            page_num = 0
            
        # Ensure text is a string
        text = str(text).strip()
        if not text:  # Skip empty texts
            return []
        
        # Combine all patterns for splitting
        all_patterns = '|'.join(self.section_breaks + self.semantic_markers)
        chunks = []
        
        # Clean the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Split by patterns
        potential_chunks = re.split(f'({all_patterns})', text)
        
        current_chunk = ""
        for i in range(0, len(potential_chunks), 2):
            chunk = potential_chunks[i]
            if i + 1 < len(potential_chunks):
                chunk += potential_chunks[i + 1]
            
            if len(current_chunk) + len(chunk) > self.max_chunk_size and current_chunk:
                if len(current_chunk) >= self.min_chunk_size:
                    chunks.append({
                        'text': current_chunk.strip(),
                        'type': 'section',
                        'size': len(current_chunk),
                        'source': source,
                        'page': page_num
                    })
                current_chunk = chunk
            else:
                current_chunk += chunk
        
        if current_chunk and len(current_chunk) >= self.min_chunk_size:
            chunks.append({
                'text': current_chunk.strip(),
                'type': 'section',
                'size': len(current_chunk),
                'source': source,
                'page': page_num
            })
        
        return chunks

    def text_to_chunks(self, texts: List[str]) -> List[Dict]:
        """Convert a list of texts into meaningful chunks using multiple strategies."""
        self.logger.info(f"Converting {len(texts)} texts to chunks...")
        
        # Convert texts to the format expected by _process_single_text
        text_infos = [
            {'text': text, 'source': 'direct_input', 'page': i}
            for i, text in enumerate(texts)
        ]
        
        # Use process pool for CPU-intensive operations
        with ProcessPoolExecutor(max_workers=self.resource_config.num_cpus) as pool:
            # Use tqdm to show progress of chunk processing
            chunk_lists = list(tqdm(
                pool.map(self._process_single_text, text_infos),
                total=len(text_infos),
                desc="Creating chunks",
                unit="text"
            ))
        
        # Flatten the results
        chunks = [chunk for sublist in chunk_lists for chunk in sublist]
        
        # Show progress for chunk merging
        with tqdm(total=len(chunks), desc="Merging chunks", unit="chunk") as pbar:
            merged_chunks = self._merge_chunks(chunks, pbar)
        
        return merged_chunks

    def _merge_chunks(self, chunks: List[Dict], pbar=None) -> List[Dict]:
        """Merge chunks while maintaining semantic coherence."""
        merged_chunks = []
        current_merged = ""
        current_metadata = {
            'sources': set(),
            'pages': set()
        }
        
        for chunk in chunks:
            if pbar is not None:
                pbar.update(1)
                
            # Check if merging would exceed max size
            if len(current_merged) + len(chunk['text']) <= self.max_chunk_size:
                # Check for semantic coherence
                if self._is_semantically_coherent(current_merged, chunk['text']):
                    current_merged += " " + chunk['text']
                    current_metadata['sources'].add(chunk['source'])
                    current_metadata['pages'].add((chunk['source'], chunk['page']))
                else:
                    if current_merged:
                        merged_chunks.append({
                            'text': current_merged.strip(),
                            'type': 'merged_section',
                            'size': len(current_merged),
                            'sources': list(current_metadata['sources']),
                            'pages': list(current_metadata['pages'])
                        })
                    current_merged = chunk['text']
                    current_metadata = {
                        'sources': {chunk['source']},
                        'pages': {(chunk['source'], chunk['page'])}
                    }
            else:
                if current_merged:
                    merged_chunks.append({
                        'text': current_merged.strip(),
                        'type': 'merged_section',
                        'size': len(current_merged),
                        'sources': list(current_metadata['sources']),
                        'pages': list(current_metadata['pages'])
                    })
                current_merged = chunk['text']
                current_metadata = {
                    'sources': {chunk['source']},
                    'pages': {(chunk['source'], chunk['page'])}
                }
        
        if current_merged:
            merged_chunks.append({
                'text': current_merged.strip(),
                'type': 'merged_section',
                'size': len(current_merged),
                'sources': list(current_metadata['sources']),
                'pages': list(current_metadata['pages'])
            })
        
        return merged_chunks

    def _is_semantically_coherent(self, text1: str, text2: str) -> bool:
        """
        Check if two text chunks are semantically coherent enough to be merged.
        Returns False if text2 contains separation words, True if it contains cohesive words.
        
        Args:
            text1: First text chunk
            text2: Second text chunk
            
        Returns:
            Boolean indicating if chunks are semantically coherent
        """
        # Words that indicate the text should be a separate chunk
        separation_words = [
            'introduction', 'background', 'overview', 'summary',
            'conclusion', 'recommendations', 'next steps',
            'first', 'second', 'third', 'finally',
            'in conclusion', 'to summarize', 'in summary',
            'chapter', 'section', 'part',
            'note:', 'important:', 'warning:',
            'key points:', 'main points:',
            'objectives:', 'goals:', 'aims:',
            'methodology:', 'approach:', 'strategy:',
            'results:', 'findings:', 'analysis:',
            'discussion:', 'implications:', 'impact:',
            'future work:', 'next steps:', 'recommendations:'
        ]
        
        # Words that indicate reference to previous context
        cohesive_words = [
            # Demonstratives
            'this', 'that', 'these', 'those',
            # Personal pronouns
            'he', 'him', 'his', 'she', 'her', 'hers',
            'it', 'its', 'they', 'them', 'their', 'theirs',
            'we', 'us', 'our', 'ours',
            # Relative pronouns
            'which', 'who', 'whom', 'whose',
            # Possessive pronouns
            'mine', 'yours', 'his', 'hers', 'its', 'ours', 'theirs',
            # Reflexive pronouns
            'myself', 'yourself', 'himself', 'herself', 'itself',
            'ourselves', 'yourselves', 'themselves',
            # Indefinite pronouns
            'one', 'ones', 'such', 'same',
            # Demonstrative adjectives
            'this', 'that', 'these', 'those',
            # Possessive adjectives
            'my', 'your', 'his', 'her', 'its', 'our', 'their',
            # Reference words
            'former', 'latter', 'above', 'below', 'aforementioned',
            'aforesaid', 'preceding', 'previous', 'prior',
            # Temporal reference
            'now', 'then', 'previously', 'earlier', 'before',
            'after', 'subsequently', 'later'
        ]
        
        # Convert text2 to lowercase for case-insensitive matching
        text2_lower = text2.lower()
        
        # First check for separation words - if found, return False
        for word in separation_words:
            if word in text2_lower:
                return False
        
        # Then check for cohesive words - if found, return True
        for word in cohesive_words:
            if word in text2_lower:
                return True
        
        # If no cohesive words are found, return False
        return False

    #def pdf_to_text(self, pdf_path):
        #

    # strings might be too long for the LLM to handle, so we need to split them into chunks
    
