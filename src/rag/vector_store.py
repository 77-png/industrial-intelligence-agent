import chromadb


class VectorStore:

    def __init__(self, persist_directory="data/chroma"):
        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name="industrial_knowledge"
        )

    def add_documents(self, chunks, embeddings):

        ids = [
            f"{chunk['source']}_page_{chunk['page']}_{i}"
            for i, chunk in enumerate(chunks)
        ]

        documents = [
            chunk["text"]
            for chunk in chunks
        ]

        metadatas = [
            {
                "source": chunk["source"],
                "page": chunk["page"]
            }
            for chunk in chunks
        ]

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

    def search(self, query_embedding, top_k=3):

        results = self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=top_k
        )

        return results

    def count(self):

        return self.collection.count()