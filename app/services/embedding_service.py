import json
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from app.config import Settings
from app.utils.timer import timed
from app.services.logging_service import get_logger

logger = get_logger(__name__)

EMBEDDING_DIMENSION = 1536  # Titan Embed Text V2 default


class EmbeddingService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = None

    def _get_client(self):
        if self._client is None:
            self._client = boto3.client(
                "bedrock-runtime",
                region_name=self.settings.AWS_REGION,
                aws_access_key_id=self.settings.AWS_ACCESS_KEY_ID or None,
                aws_secret_access_key=self.settings.AWS_SECRET_ACCESS_KEY or None,
            )
        return self._client

    async def embed(self, text: str) -> list[float]:
        """Embed a single text string using Amazon Titan Embeddings V2."""
        client = self._get_client()
        body = json.dumps({"inputText": text[:8000]})  # Titan max input

        with timed("bedrock_embed") as t:
            try:
                response = client.invoke_model(
                    modelId=self.settings.BEDROCK_EMBEDDING_MODEL_ID,
                    body=body,
                    contentType="application/json",
                    accept="application/json",
                )
            except NoCredentialsError:
                raise RuntimeError("AWS credentials not configured.")
            except ClientError as e:
                code = e.response["Error"]["Code"]
                logger.error("Embedding ClientError", code=code, error=str(e))
                raise

        result = json.loads(response["body"].read())
        embedding = result.get("embedding", [])

        logger.info(
            "embed_complete",
            dim=len(embedding),
            latency_ms=t.get("elapsed_ms", 0.0),
        )
        return embedding

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts one by one (Titan V2 has no batch endpoint)."""
        embeddings = []
        for i, text in enumerate(texts):
            emb = await self.embed(text)
            embeddings.append(emb)
            if (i + 1) % 10 == 0:
                logger.info("embed_batch_progress", done=i + 1, total=len(texts))
        return embeddings
