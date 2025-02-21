# utils/embeddings.py
import openai
import numpy as np

def get_embedding(text: str) -> np.ndarray:
    """
    Obtém o embedding para o texto fornecido usando a API de embeddings do OpenAI.
    Exemplo utiliza o modelo "text-embedding-ada-002".
    """
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embedding = response['data'][0]['embedding']
    return np.array(embedding)

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Calcula a similaridade coseno entre dois vetores.
    """
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)

# Cache global para armazenar os embeddings das causas
_cached_candidate_embeddings = {}

def cache_candidate_embeddings(causes: list) -> dict:
    """
    Para cada causa na lista, calcula e armazena seu embedding. Se já estiver cacheado, retorna o cache.
    """
    global _cached_candidate_embeddings
    if _cached_candidate_embeddings:
        return _cached_candidate_embeddings
    for cause in causes:
        _cached_candidate_embeddings[cause] = get_embedding(cause)
    return _cached_candidate_embeddings
