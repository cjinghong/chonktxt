import unittest
import os
from chonktxt import Chonktxt

class TestChonktxt(unittest.TestCase):
    def test_situate_context(self):
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        client = Chonktxt(anthropic_api_key=anthropic_api_key)
        client.use_doc_pdf("./tests/sample-tenancy-agreement.pdf")
        chunks = [
            "The Landlord has the right not to renew the rental period",
            """
            RM2,600 
            RM650 
            
            RM1,300 
            
            RM4,550
            """
        ]

        chunk_with_context, token_counts = client.contextualize_chunks(chunks, parallel_threads=1)

        # Print usage summary
        print(f"Total input tokens without caching: {token_counts['input']}")
        print(f"Total output tokens: {token_counts['output']}")
        print(f"Total input tokens written to cache: {token_counts['cache_creation']}")
        print(f"Total input tokens read from cache: {token_counts['cache_read']}")
        
        total_tokens = token_counts['input'] + token_counts['cache_read'] + token_counts['cache_creation']
        savings_percentage = (token_counts['cache_read'] / total_tokens) * 100 if total_tokens > 0 else 0
        print(f"Total input token savings from prompt caching: {savings_percentage:.2f}% of all input tokens used were read from cache.")
        print("Tokens read from cache come at a 90 percent discount!")


        # First contextualized chunk should include "AGREEMENT BETWEEN LANDLORD AND TENANT"
        self.assertTrue("AGREEMENT BETWEEN LANDLORD AND TENANT" in chunk_with_context[0]['contextualized_chunk'])

        # Second contextualized chunk should include words like 
        # "initial payment", "deposit", "utility deposit", "advance rental"
        words_to_check = [
            "initial payment",
            "deposit",
            "utility deposit",
            "advance rental"
        ]

        for word in words_to_check:
            self.assertTrue(word in chunk_with_context[1]['contextualized_chunk'])
    

if __name__ == "__main__":
    unittest.main()