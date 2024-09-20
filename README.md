## Overview

Chonktxt is an SDK that makes it easy to do contextual chunking. Inspired by the [contextual retrieval article](https://www.anthropic.com/news/contextual-retrieval) by Anthropic.

Pass in a PDF or text file, and Chonktxt will return the original chunk + contextualized chunk.

## Installation

```bash
pip install chonktxt
```

## Usage

```python
from chonktxt import Chonktxt

client = Chonktxt(anthropic_api_key=YOUR_ANTHROPIC_API_KEY)

# Use a PDF file as the source document
client.use_doc_pdf("./large-pdf.pdf")

# Or use text as the source document
client.use_doc_txt("This is a very very long text")

# Get contextualized chunks
contextualized_chunks, token_counts = client.contextualize_chunks(
    chunks=[
        "Chain-of-Thought (Wei et al., 2022) 28.0 ±3.1 34.9 ±3.2 15.0 ±2.5 77.8 ±2.8 88.9 ±2.2",
    ],

    # Use 1 thread if this is the first time you're using a specific document
    # this way we can be sure that anthropic has cached the document
    # feel free to increase this number on subsequent calls
    parallel_threads=1
)

print(contextualized_chunks)
# output:
# [
#     {
#         "original_chunk": "Chain-of-Thought (Wei et al., 2022) 28.0 ±3.1 34.9 ±3.2 15.0 ±2.5 77.8 ±2.8 88.9 ±2.2",
#         "contextualized_chunk": "This chunk presents the performance of the Chain-of-Thought baseline agent on various benchmarks, including reading comprehension (MGSM), math (GSM8K, GSM-Hard, SVAMP, ASDiv), and multi-task (MMLU) domains."
#     },
# ]

# As we can see from the above output, the original chunk is meaningless numbers on its own, but the contextualized chunk contains meaningful text.

# We can also print usage summary
print(f"Total input tokens without caching: {token_counts['input']}")
print(f"Total output tokens: {token_counts['output']}")
print(f"Total input tokens written to cache: {token_counts['cache_creation']}")
print(f"Total input tokens read from cache: {token_counts['cache_read']}")

total_tokens = token_counts['input'] + token_counts['cache_read'] + token_counts['cache_creation']
savings_percentage = (token_counts['cache_read'] / total_tokens) * 100 if total_tokens > 0 else 0
print(f"Total input token savings from prompt caching: {savings_percentage:.2f}% of all input tokens used were read from cache.")
print("Tokens read from cache come at a 90 percent discount!")
```