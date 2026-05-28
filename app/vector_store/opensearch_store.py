"""
OpenSearch vector store — Phase 13 AWS upgrade.
Implements the same interface as ChromaStore for a drop-in swap.
"""


class OpenSearchStore:
    def __init__(self, settings) -> None:
        raise NotImplementedError(
            "OpenSearchStore — implement in Phase 13 (AWS upgrade). "
            "Set VECTOR_STORE_TYPE=chroma in .env to use ChromaDB."
        )

    def upsert(self, chunk_id, text, metadata, embedding): ...
    def upsert_batch(self, chunk_ids, texts, metadatas, embeddings): ...
    def query(self, query_embedding, top_k=5, where=None): ...
    def delete_by_doc_id(self, doc_id): ...
    def count(self): ...
