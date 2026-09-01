from loader import load_documents
from splitter import split_documents
from retriever import KnowledgeBase

if __name__ == "__main__":
    docs = load_documents()
    chunks = split_documents(docs)
    
    kb = KnowledgeBase()
    kb.add_documents(chunks)
    
    test_questions = [
        "工作6年有多少天年假？",
        "年假可以延期到什么时候？"
    ]
    
    for q in test_questions:
        print(f"\n{'='*50}")
        print(f"❓ 问题: {q}")
        results = kb.search(q, top_k=2)
        print(f"📄 检索结果 (Top-2):")
        for idx, res in enumerate(results):
            print(f"\n  第 {idx+1} 条 (相似度距离: {res['score']:.4f}):")
            print(f"  内容: {res['content']}")
            print(f"  来源: {res['metadata']}")