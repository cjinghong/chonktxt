import anthropic
from pdfminer.high_level import extract_text
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import threading

DOCUMENT_CONTEXT_PROMPT = """
<document>
{doc_content}
</document>
"""

CHUNK_CONTEXT_PROMPT = """
Here is the chunk we want to situate within the whole document
<chunk>
{chunk_content}
</chunk>

Please give a short succinct context to situate this chunk within the overall document for the purposes of improving search retrieval of the chunk.
Answer only with the succinct context and nothing else.
"""

class Chonktxt:
    def __init__(self, anthropic_api_key: str):
        self.anthropic_client = anthropic.Anthropic(
            api_key=anthropic_api_key,
        )
        self.token_counts = {
            'input': 0,
            'output': 0,
            'cache_read': 0,
            'cache_creation': 0
        }
        self.token_lock = threading.Lock()
        self.doc = None


    def use_doc_str(self, doc: str):
        self.doc = doc

    def use_doc_pdf(self, file_path: str):
        text = extract_text(file_path)
        self.doc = text


    """
    Given a chunk, situates it within the context of the document.
    """
    def situate_context(self, chunk: str):
        if not self.doc:
            raise ValueError("Please provide a source document using `use_doc_str` or `use_doc_pdf`")

        response = self.anthropic_client.beta.prompt_caching.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            temperature=0.0,
            messages=[
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text",
                            "text": DOCUMENT_CONTEXT_PROMPT.format(doc_content=self.doc),
                            "cache_control": {"type": "ephemeral"}
                        },
                        {
                            "type": "text",
                            "text": CHUNK_CONTEXT_PROMPT.format(chunk_content=chunk),
                        }
                    ]
                }
            ],
            extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"}
        )
        return response.content[0].text, response.usage
    
    """
    Given a list of chunks, situates each chunk within the context of the document, with parallelization.
    """
    def contextualize_chunks(self, chunks: list[str], parallel_threads: int = 1) -> tuple[list[dict[str, str]], dict[str, int]]:
        def process_chunk(chunk: str):
            contextualized_text, usage = self.situate_context(chunk)
            with self.token_lock:
                self.token_counts['input'] += usage.input_tokens
                self.token_counts['output'] += usage.output_tokens
                self.token_counts['cache_read'] += usage.cache_read_input_tokens
                self.token_counts['cache_creation'] += usage.cache_creation_input_tokens
            
            return {
                'original_chunk': chunk,
                'contextualized_chunk': contextualized_text
            }

        total_chunks = len(chunks)
        processed_chunks = [] # dict[original_chunk: str, contextualized_chunk: str]

        print(f"Processing {total_chunks} chunks with {parallel_threads} threads")

        with ThreadPoolExecutor(max_workers=parallel_threads) as executor:
            futures = []
            for chunk in chunks:
                futures.append(executor.submit(process_chunk, chunk))
            
            for future in tqdm(as_completed(futures), total=total_chunks, desc="Processing chunks"):
                result = future.result()
                processed_chunks.append(result)

        return processed_chunks, self.token_counts
    