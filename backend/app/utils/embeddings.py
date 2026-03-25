from sentence_transformers import SentenceTransformer

from app.config import settings


class EmbeddingService:
    _instance: "EmbeddingService | None" = None
    _model: SentenceTransformer | None = None

    @classmethod
    def get_instance(cls) -> "EmbeddingService":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if EmbeddingService._model is None:
            EmbeddingService._model = SentenceTransformer(settings.embedding_model_name)

    @property
    def model(self) -> SentenceTransformer:
        return EmbeddingService._model  # type: ignore

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()

    def embed_single(self, text: str) -> list[float]:
        return self.model.encode(text, show_progress_bar=False).tolist()
