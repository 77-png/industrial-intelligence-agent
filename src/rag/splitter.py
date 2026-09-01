from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents: list[dict]) -> list[dict]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " "]
    )
    chunks = []
    for document in documents:
        split_texts = text_splitter.split_text(document["text"])

        for text in split_texts:
            chunks.append(
                {
                    "text": text,
                    "source": document["source"],
                    "page": document["page"],
                }
            )
    return chunks