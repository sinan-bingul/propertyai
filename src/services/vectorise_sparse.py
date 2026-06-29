from typing import Dict, List, Tuple
from collections import Counter
import math
import re


class SparseVector:
    """BM25 sparse vectorization service.

    BM25 (Best Matching 25) is a ranking function used for information retrieval
    that produces sparse vector representations based on term frequency and
    inverse document frequency.
    """

    def __init__(
        self,
        corpus: List[str] | None = None,
        k1: float = 1.5,
        b: float = 0.75
    ):
        """Initialize BM25 sparse vectorizer.

        Args:
            corpus: List of documents to compute IDF statistics. If None, uses single-doc mode.
            k1: Term frequency saturation parameter (default: 1.5)
            b: Length normalization parameter (default: 0.75)
        """
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.vocab: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.avgdl = 0.0

        if corpus:
            self._build_vocabulary()
            self._compute_idf()

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into lowercase words."""
        # Simple word tokenization: lowercase, split on non-alphanumeric
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def _build_vocabulary(self):
        """Build vocabulary from corpus."""
        vocab_set = set()
        total_length = 0

        for doc in self.corpus:
            tokens = self._tokenize(doc)
            vocab_set.update(tokens)
            total_length += len(tokens)

        self.vocab = {word: idx for idx, word in enumerate(sorted(vocab_set))}
        self.avgdl = total_length / len(self.corpus) if self.corpus else 0

    def _compute_idf(self):
        """Compute inverse document frequency for each term in vocabulary."""
        N = len(self.corpus)
        doc_freq = Counter()

        for doc in self.corpus:
            tokens = set(self._tokenize(doc))
            doc_freq.update(tokens)

        # IDF formula: log((N - df + 0.5) / (df + 0.5) + 1)
        for term in self.vocab:
            df = doc_freq.get(term, 0)
            self.idf[term] = math.log((N - df + 0.5) / (df + 0.5) + 1.0)

    def _compute_bm25_scores(self, text: str) -> Dict[str, float]:
        """Compute BM25 scores for each term in the text.

        BM25 formula:
        score(term) = IDF(term) * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (dl / avgdl)))

        where:
        - tf: term frequency in document
        - dl: document length
        - avgdl: average document length in corpus
        """
        tokens = self._tokenize(text)
        doc_length = len(tokens)
        term_freq = Counter(tokens)
        scores = {}

        for term, tf in term_freq.items():
            # If corpus was provided, use computed IDF; otherwise use default IDF
            if self.corpus:
                idf = self.idf.get(term, 0.0)
                avgdl = self.avgdl
            else:
                # Single document mode: use simplified IDF
                idf = 1.0
                avgdl = doc_length

            # BM25 scoring formula
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * (doc_length / avgdl if avgdl > 0 else 1))
            score = idf * (numerator / denominator)

            if score > 0:  # Only include non-zero scores (sparse vector)
                scores[term] = score

        return scores

    async def run(self, input_text: str) -> Dict[str, float]:
        """Convert input text to BM25 sparse vector.

        Args:
            input_text: Text to vectorize

        Returns:
            Dictionary mapping terms to their BM25 scores (sparse representation)
        """
        return self._compute_bm25_scores(input_text)

    def run_sync(self, input_text: str) -> Dict[str, float]:
        """Synchronous version of run method."""
        return self._compute_bm25_scores(input_text)

    def to_indexed_vector(self, input_text: str) -> List[Tuple[int, float]]:
        """Convert input text to indexed sparse vector.

        Args:
            input_text: Text to vectorize

        Returns:
            List of (token_id, score) tuples for non-zero scores
        """
        if not self.vocab:
            raise ValueError("Vocabulary not initialized. Provide corpus during initialization.")

        scores = self._compute_bm25_scores(input_text)
        indexed_vector = []

        for term, score in scores.items():
            if term in self.vocab:
                token_id = self.vocab[term]
                indexed_vector.append((token_id, score))

        # Sort by token_id for consistency
        indexed_vector.sort(key=lambda x: x[0])
        return indexed_vector


if __name__ == "__main__":
    import asyncio
    from logger import logging

    # Example 1: Single document mode (no corpus)
    vectorizer = SparseVector()
    text = "The quick brown fox jumps over the lazy dog"

    # Async usage
    sparse_vector = asyncio.run(vectorizer.run(text))
    logging.info(f"Sparse vector (term -> score): {sparse_vector}")

    # Example 2: With corpus for better IDF computation
    corpus = [
        "The quick brown fox jumps over the lazy dog",
        "A fast brown fox leaps over a sleepy dog",
        "The dog was lazy and slept all day"
    ]

    vectorizer_with_corpus = SparseVector(corpus=corpus)
    query = "quick fox"

    sparse_vector_with_idf = asyncio.run(vectorizer_with_corpus.run(query))
    logging.info(f"Sparse vector with IDF: {sparse_vector_with_idf}")

    # Example 3: Indexed vector format
    indexed_vector = vectorizer_with_corpus.to_indexed_vector(query)
    logging.info(f"Indexed sparse vector: {indexed_vector}")
