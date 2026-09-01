from src.rag.pipeline import RAGPipeline


rag = None


def knowledge_search(question: str) -> dict:

    global rag

    if rag is None:
        rag = RAGPipeline()

    results = rag.search(
        question,
        top_k=3
    )

    contexts = []
    sources = []

    for document, metadata in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):

        contexts.append(
            f"""
来源：{metadata['source']}
页码：{metadata['page']}

内容：
{document}
"""
        )

        sources.append({
            "source": metadata["source"],
            "page": metadata["page"]
        })

    return {
        "content": "\n\n".join(contexts),
        "sources": sources
    }