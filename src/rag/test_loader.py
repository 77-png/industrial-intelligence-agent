from loader import load_documents
from splitter import split_documents

if __name__ == "__main__":
    docs = load_documents()
    
    chunks = split_documents(docs)

    print("\n--- 预览前 3 个文本块 ---")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n块 {i+1}:")
        print(chunk.page_content)
        print(f"元数据: {chunk.metadata}")