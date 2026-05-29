"""
Phase 4 — Embed all processed chunks and store in ChromaDB.
Run AFTER ingest_documents.py.
Run: python scripts/embed_and_store.py
"""
import asyncio
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.config import settings
from app.services.embedding_service import EmbeddingService, INTER_REQUEST_DELAY
from app.vector_store.chroma_store import ChromaStore
from app.data_pipeline.ingestion_pipeline import load_all_chunks

DELAY = INTER_REQUEST_DELAY  # 2s between calls — respects new-account rate limits


async def main():
    chunks = load_all_chunks()
    if not chunks:
        print("No chunks found. Run scripts/ingest_documents.py first.")
        return

    print(f"Found {len(chunks)} chunks to embed.")
    print(f"Embedding model : {settings.BEDROCK_EMBEDDING_MODEL_ID}")
    print(f"Region          : {settings.AWS_REGION}")
    print(f"Delay between calls: {DELAY}s  (estimated time: ~{len(chunks)*DELAY/60:.1f} min)")
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
            metadata = {k: v for k, v in chunk.items() if k != "text"}
            store.upsert(
                chunk_id=chunk["chunk_id"],
                text=chunk["text"],
                metadata=metadata,
                embedding=embedding,
            )
            success += 1
            print(f"  [{i+1:>2}/{len(chunks)}] OK  {chunk.get('source_file', '')}  chunk_{chunk.get('chunk_index', '')}")
        except Exception as e:
            failed += 1
            print(f"  [{i+1:>2}/{len(chunks)}] ERROR: {e}")

        # Delay between calls to respect rate limits (skip after last chunk)
        if i < len(chunks) - 1:
            time.sleep(DELAY)

    print(f"\nDone.  Stored: {success}  Failed: {failed}")
    print(f"ChromaDB total vectors: {store.count()}")
    if success == len(chunks):
        print("\nPhase 4 PASSED — all chunks embedded and stored.")


if __name__ == "__main__":
    asyncio.run(main())
