# src/rag/retriever.py
import chromadb
from chromadb.utils import embedding_functions
from embedding import get_embeddings

class KnowledgeBase:
    def __init__(self, collection_name="company_kb"):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=None
        )
        print(f"✅ 连接向量数据库成功，当前集合: {collection_name}")
    
    def add_documents(self, chunks):
        ids = []
        documents = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            doc_id = f"chunk_{i}"
            ids.append(doc_id)
            documents.append(chunk.page_content)
            metadatas.append(chunk.metadata)
        
        print(f"⏳ 正在生成 {len(documents)} 个文本块的向量...")
        embeddings = get_embeddings(documents)
        
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        print(f"✅ 成功存入 {len(documents)} 个文档块到向量库")
    
    def search(self, query: str, top_k=3):
        print(f"⏳ 正在搜索: {query}")
        query_embedding = get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        retrieved = []
        if results['documents'] and len(results['documents']) > 0:
            for i in range(len(results['documents'][0])):
                retrieved.append({
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'score': results['distances'][0][i] 
                })
        return retrieved