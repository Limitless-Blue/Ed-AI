from pathlib import Path
from typing import List

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from google import genai

from app.config import settings

# Cache loaded stores so we don't re-embed on every request
_stores: dict[str, Chroma | None] = {}

_genai_client = genai.Client(api_key=settings.google_api_key)
_EMBED_MODEL  = "models/gemini-embedding-001"


class _GeminiEmbeddings(Embeddings):
    """Thin LangChain-compatible wrapper around the google.genai embedding endpoint."""

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        result = _genai_client.models.embed_content(model=_EMBED_MODEL, contents=texts)
        return [list(e.values) for e in result.embeddings]

    def embed_query(self, text: str) -> List[float]:
        result = _genai_client.models.embed_content(model=_EMBED_MODEL, contents=[text])
        return list(result.embeddings[0].values)


_embeddings = _GeminiEmbeddings()


def _build_store(key: str, content_path: Path) -> Chroma | None:
    persist_dir = str(settings.chroma_dir / key)
    loader = DirectoryLoader(
        str(content_path), glob="**/*.md",
        loader_cls=TextLoader, silent_errors=True,
        loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()
    if not docs:
        return None
    chunks = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100).split_documents(docs)
    try:
        return Chroma.from_documents(chunks, _embeddings, persist_directory=persist_dir)
    except Exception:
        return None


def _get_store(course_id: str | None) -> Chroma | None:
    # Only build per-course stores; skip global indexing to avoid rate limits
    if not course_id:
        return None
    if course_id not in _stores:
        path = settings.content_dir / "courses" / course_id
        if not path.exists():
            _stores[course_id] = None
            return None
        _stores[course_id] = _build_store(course_id, path)
    return _stores[course_id]


async def retrieve_chunks(query: str, course_id: str | None = None) -> list[str]:
    try:
        store = _get_store(course_id)
        if not store:
            return []
        docs = store.similarity_search(query, k=4)
        return [d.page_content for d in docs]
    except Exception:
        return []
