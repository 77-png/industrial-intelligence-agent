from rag.loader import load_all_pdfs
from rag.splitter import split_documents
from rag.embedding import EmbeddingModel
from rag.vector_store import VectorStore
from rag.generator import RAGGenerator


def build_knowledge_base():

    print("开始构建知识库...")

    # 1. PDF → Text
    documents = load_all_pdfs(
        "data/documents"
    )

    print(f"读取完成：{len(documents)} 个页面")

    # 2. Text → Chunks
    chunks = split_documents(
        documents
    )

    print(f"切分完成：{len(chunks)} 个 chunks")

    # 3. Embedding
    embedding_model = EmbeddingModel()

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = embedding_model.encode(
        texts
    )

    print(
        f"Embedding完成：{len(embeddings)} 个向量"
    )

    # 4. Chroma
    vector_store = VectorStore()

    vector_store.add_documents(
        chunks,
        embeddings
    )

    print(
        f"知识库构建完成，共 "
        f"{vector_store.count()} 条数据"
    )


def test_rag():

    embedding_model = EmbeddingModel()

    vector_store = VectorStore()

    generator = RAGGenerator()

    question = input(
        "\n请输入问题："
    )

    # Query → Embedding
    query_embedding = embedding_model.encode(
        [question]
    )[0]

    # Retrieval
    results = vector_store.search(
        query_embedding,
        top_k=3
    )

    print("\n========== 检索结果 ==========")

    for i, (document, metadata) in enumerate(
        zip(
            results["documents"][0],
            results["metadatas"][0]
        )
    ):

        print(
            f"\n--- Result {i + 1} ---"
        )

        print(
            f"来源：{metadata['source']}"
        )

        print(
            f"页码：{metadata['page']}"
        )

        print(
            f"内容：{document[:300]}"
        )

    # Generation
    answer = generator.generate(
        question,
        results
    )

    print(
        "\n========== RAG答案 =========="
    )

    print(answer)


from agent.agent import Agent


if __name__ == "__main__":

    agent = Agent()

    while True:

        question = input("\n用户：")

        if question.lower() in ["exit", "quit"]:
            break

        answer = agent.run(question)

        print("\nAgent：")
        print(answer)