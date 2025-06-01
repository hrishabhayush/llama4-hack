# return list of strings
from PyPDF2 import PdfReader
import re
from typing import List, Dict

class Preprocessor:
    def __init__(self):
        # Define chunking parameters
        self.min_chunk_size = 100
        self.max_chunk_size = 2000
        
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

    def process_pdfs(self, sources):
        # for each pdf in sources, convert to text, a list of strings from each page
        text = []
        for source in sources:
            text.extend(self.process_1_pdf(source))
        return text
    
    def process_1_pdf(self, source):
        # for a source, convert to text, a list of strings from each page
        text = []
        reader = PdfReader(source)
        #loop through all the pages in the reader
        for page in reader.pages:
            text.append(page.extract_text()) 
        return text

    def text_to_chunks(self, texts: List[str]) -> List[Dict]:
        """
        Convert a list of texts into meaningful chunks using multiple strategies.
        
        Args:
            texts: List of text strings from each page
            
        Returns:
            List of dictionaries containing chunks with metadata
        """
        chunks = []
        
        # Combine all patterns for splitting
        all_patterns = '|'.join(self.section_breaks + self.semantic_markers)
        
        for page_num,text in enumerate(texts):
            # Clean the text
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Split by patterns
            potential_chunks = re.split(f'({all_patterns})', text)
            
            current_chunk = ""
            for i in range(0, len(potential_chunks), 2):
                chunk = potential_chunks[i]
                if i + 1 < len(potential_chunks):
                    chunk += potential_chunks[i + 1]  # Add the separator back
                
                # If adding this chunk would exceed max size, save current and start new
                if len(current_chunk) + len(chunk) > self.max_chunk_size and current_chunk:
                    if len(current_chunk) >= self.min_chunk_size:
                        chunks.append({
                            'text': current_chunk.strip(),
                            'type': 'section',
                            'size': len(current_chunk)
                        })
                    current_chunk = chunk
                else:
                    current_chunk += chunk
            
            # Add the last chunk if it meets minimum size
            if current_chunk and len(current_chunk) >= self.min_chunk_size:
                chunks.append({
                    'text': current_chunk.strip(),
                    'type': 'section',
                    'size': len(current_chunk)
                })
        
        # Post-processing: Merge small chunks and ensure semantic coherence
        merged_chunks = []
        current_merged = ""
        
        for chunk in chunks:
            # Check if merging would exceed max size
            if len(current_merged) + len(chunk['text']) <= self.max_chunk_size:
                # Check for semantic coherence
                if self._is_semantically_coherent(current_merged, chunk['text']):
                    current_merged += " " + chunk['text']
                else:
                    if current_merged:
                        merged_chunks.append({
                            'text': current_merged.strip(),
                            'type': 'merged_section',
                            'size': len(current_merged)
                        })
                    current_merged = chunk['text']
            else:
                if current_merged:
                    merged_chunks.append({
                        'text': current_merged.strip(),
                        'type': 'merged_section',
                        'size': len(current_merged)
                    })
                current_merged = chunk['text']
        
        if current_merged:
            merged_chunks.append({
                'text': current_merged.strip(),
                'type': 'merged_section',
                'size': len(current_merged)
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
    
