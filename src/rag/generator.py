from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


class RAGGenerator:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

    def generate(self, question, results):

        contexts = []

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

        context = "\n\n".join(contexts)

        prompt = f"""
请根据下面提供的知识库内容回答用户问题。

要求：
1. 只能根据知识库内容回答。
2. 不要编造知识库中没有的信息。
3. 如果知识库中没有足够的信息，请明确说明。
4. 回答要简洁、准确。
5. 最后列出参考来源。

知识库内容：
{context}

用户问题：
{question}
"""

        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个企业工业知识库问答助手。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content