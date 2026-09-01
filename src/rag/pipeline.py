from rag.embedding import EmbeddingModel
from rag.vector_store import VectorStore
from rag.generator import RAGGenerator


class RAGPipeline:

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore()

        self.generator = RAGGenerator()

    def search(self, question, top_k=3):

        query_embedding = self.embedding_model.encode(
            [question]
        )[0]

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        return results

    def answer(self, question, top_k=3):

        results = self.search(
            question,
            top_k=top_k
        )

        answer = self.generator.generate(
            question,
            results
        )

        return answer, results