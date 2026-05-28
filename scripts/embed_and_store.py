"""
Phase 4 — Embed all processed chunks and store in ChromaDB.
Run AFTER ingest_documents.py.
Run: python scripts/embed_and_store.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.config import settings
from app.services.embedding_service import EmbeddingService
from app.vector_store.chroma_store import ChromaStore
from app.data_pipeline.ingestion_pipeline import load_all_chunks


async def main():
    chunks = load_all_chunks()
    if not chunks:
        print("No chunks found. Run scripts/ingest_documents.py first.")
        return

    print(f"Found {len(chunks)} chunks to embed.")
    print(f"Embedding model : {settings.BEDROCK_EMBEDDING_MODEL_ID}")
    print(f"Region          : {settings.AWS_REGION}")
    print()

    embedding_svc = EmbeddingService(settings)
    store = ChromaStore(settings)

    existing = store.count()
    if existing > 0:
        print(f"ChromaDB already has {existing} vectors. Upserting (safe to re-run).")

    success, failed = 0, 0
    for i, chunk in enumerate(chunks):
        try:
            embedding = await embedding_svc.embed(chunk["text"])
            metadata = {k: v for k, v in chunk.items() if k not in ("text",)}
            store.upsert(
                chunk_id=chunk["chunk_id"],
                text=chunk["text"],
                metadata=metadata,
                embedding=embedding,
            )
            success += 1
            if (i + 1) % 5 == 0 or (i + 1) == len(chunks):
                print(f"  [{i+1}/{len(chunks)}] embedded and stored")
        except Exception as e:
            failed += 1
            print(f"  ERROR on chunk {chunk['chunk_id']}: {e}")

    print(f"\nDone. Stored: {success}  Failed: {failed}")
    print(f"ChromaDB total vectors: {store.count()}")


if __name__ == "__main__":
    asyncio.run(main())
