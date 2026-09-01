from openai import OpenAI
import os
import json
from dotenv import load_dotenv

from tools.knowledge_tool import knowledge_search
from tools.sql_tool import sql_query

load_dotenv()


class Agent:

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

        self.tools = [

            {
                "type": "function",
                "function": {
                    "name": "knowledge_search",
                    "description": (
                        """
                        Search industrial knowledge documents.

                        Use ONLY for:
                        - industrial concepts
                        - industrial data classification
                        - industrial internet
                        - standards
                        - guidelines
                        - definitions
                        - technical explanations

                        Examples:
                        '工业数据有哪些分类'
                        '工业互联网平台是什么'
                        '工业数据如何分级'

                        Do NOT use for:
                        - sales
                        - numbers
                        - statistics
                        - database records
                        """
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "The question to search."
                            }
                        },
                        "required": ["question"]
                    }
                }
            },

            {
                "type": "function",
                "function": {
                    "name": "sql_query",
                    "description": (
                        """
                        Query structured business database.

                        Use ONLY for:
                        - sales information
                        - numerical statistics
                        - counts
                        - rankings
                        - aggregation
                        - records stored in database

                        Examples:
                        '2026销售额最高产品'
                        '总销售额是多少'
                        '有多少条记录'

                        Do NOT use for:
                        - concepts
                        - definitions
                        - industrial knowledge
                        - greetings
                        """
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": (
                                    "A read-only SQL SELECT query."
                                )
                            }
                        },
                        "required": ["query"]
                    }
                }
            }

        ]
    def run(self, question, history=None):

        if history is None:
            history = []


        messages = [
            {
                "role": "system",
                "content": """
                    你是一个企业工业智能助手。

                    你有两个工具：

                    ====================
                    工具1：knowledge_search
                    ====================

                    用途：
                    查询工业知识文档。

                    知识库包含：

                    - 工业数据分类分级指南.pdf
                    - 工业互联网平台白皮书.pdf

                    以下类型的问题必须调用 knowledge_search：

                    - 工业数据分类
                    - 工业互联网
                    - 工业平台
                    - 工业领域概念解释
                    - 标准、指南、定义类问题


                    ====================
                    工具2：sql_query
                    ====================

                    用途：
                    查询结构化业务数据。

                    数据库：

                    sales(
                        id,
                        product,
                        category,
                        sales,
                        year
                    )

                    以下问题必须调用 sql_query：

                    - 销售额
                    - 数量
                    - 排名
                    - 统计
                    - 年份数据
                    - 产品数据


                    ====================
                    工具使用规则
                    ====================

                    1. 涉及知识库内容的问题，必须调用 knowledge_search。

                    2. 涉及数据库数据的问题，必须调用 sql_query。

                    3. 不允许直接凭已有知识回答工业专业问题。

                    4. 工具返回结果后，再生成最终答案。

                    5. 当前问题如果依赖之前的对话，
                    必须结合历史对话理解用户意图。

                    6. 例如：

                    用户：
                    工业数据有哪些分类？

                    助手：
                    工业数据可以分为……

                    用户：
                    那三级数据呢？

                    此时“那三级数据”指的是上一轮讨论的
                    工业数据分类，因此应该结合上下文，
                    调用 knowledge_search。


                    ====================
                    SQL规则
                    ====================

                    如果用户询问排名：

                    例如：
                    2026销售额最高产品

                    生成：

                    SELECT product, sales
                    FROM sales
                    WHERE year=2026
                    ORDER BY sales DESC
                    LIMIT 1


                    如果用户询问统计：

                    例如：
                    2026总销售额

                    生成：

                    SELECT SUM(sales)
                    FROM sales
                    WHERE year=2026


                    ====================
                    问题分类
                    ====================

                    Category A：
                    Industrial knowledge question

                    例如：

                    - 什么是工业互联网？
                    - 工业数据有哪些分类？
                    - 工业数据如何分级？

                    → MUST use knowledge_search


                    Category B：
                    Structured data question

                    例如：

                    - 哪个产品销售最高？
                    - 2026销售额是多少？
                    - 有多少条数据？

                    → MUST use sql_query


                    Category C：
                    Casual conversation

                    例如：

                    - 你好
                    - 谢谢
                    - 你是谁

                    → MUST NOT use any tool


                    Never call sql_query for questions
                    only containing the word "数据".

                    ====================
                    多轮对话上下文理解与工具路由
                    ====================

                    处理当前用户问题时，必须结合历史对话理解用户真实意图。

                    特别注意：
                    当前问题中的代词、指代词和省略内容可能依赖上一轮对话。

                    常见指代词包括：

                    - 它
                    - 这个
                    - 这个产品
                    - 该产品
                    - 该数据
                    - 这个数据
                    - 上述产品
                    - 上述数据
                    - 上一个
                    - 刚才的
                    - 前面提到的
                    - 这个分类
                    - 这个指标


                    【第一步：上下文补全】

                    如果当前问题存在指代、省略或者上下文依赖：

                    必须先根据历史对话确定具体指代对象。

                    然后在内部将当前问题转换成一个完整的问题。

                    例如：

                    历史对话：

                    用户：
                    2026年销售额最高的产品是什么？

                    助手：
                    工业软件平台，销售额350000。

                    当前用户：
                    它属于哪类工业数据？

                    必须理解为：

                    工业软件平台属于哪类工业数据？


                    再例如：

                    历史对话：

                    用户：
                    2026年销售额最高的产品是什么？

                    助手：
                    工业软件平台，销售额350000。

                    当前用户：
                    它的销售额是多少？

                    必须理解为：

                    工业软件平台的销售额是多少？


                    【第二步：根据补全后的完整问题判断工具】

                    非常重要：

                    工具选择必须根据“补全后的完整问题”的语义，
                    而不是根据历史信息来自哪个工具。

                    例如：

                    历史问题通过 sql_query 得到了：

                    工业软件平台

                    当前问题：

                    它属于哪类工业数据？

                    虽然“工业软件平台”来自 SQL 查询结果，
                    但当前问题是在询问工业数据分类。

                    因此：

                    → 必须调用 knowledge_search。


                    反过来：

                    历史问题：

                    工业数据有哪些分类？

                    当前问题：

                    其中生产数据的销售额是多少？

                    此时当前问题是在询问结构化业务数据。

                    因此：

                    → 必须调用 sql_query。


                    【第三步：工具选择原则】

                    判断的是“当前用户真正想知道什么”。

                    如果当前问题询问：

                    - 工业概念
                    - 工业数据分类
                    - 工业数据分级
                    - 工业互联网
                    - 工业平台
                    - 标准
                    - 指南
                    - 定义
                    - 技术解释

                    → knowledge_search


                    如果当前问题询问：

                    - 销售额
                    - 数量
                    - 排名
                    - 统计
                    - 年份数据
                    - 产品数据
                    - 数据库记录

                    → sql_query


                    如果当前问题只是：

                    - 你好
                    - 谢谢
                    - 你是谁
                    - 好的

                    → 不调用工具。


                    【第四步：不要因为实体来源而错误选择工具】

                    不要因为某个实体来自 SQL 数据库，
                    就认为后续关于该实体的问题也必须使用 SQL。

                    例如：

                    SQL 查询得到：

                    工业软件平台

                    之后用户问：

                    “它属于哪类工业数据？”

                    这是知识库问题。

                    必须调用：

                    knowledge_search


                    如果 SQL 查询得到：

                    工业软件平台

                    之后用户问：

                    “它的销售额是多少？”

                    这是数据库问题。

                    必须调用：

                    sql_query


                    总结：

                    先解决：

                    “用户现在到底在问什么？”

                    再决定：

                    “应该调用哪个工具？”

                    不要根据上一轮调用过什么工具来决定当前工具。

                    ====================
                    最终决策流程
                    ====================

                    每次收到用户问题时，按照以下顺序执行：

                    Step 1.
                    阅读当前问题。

                    Step 2.
                    阅读历史对话。

                    Step 3.
                    解决当前问题中的代词和省略信息。

                    Step 4.
                    在内部形成完整问题。

                    Step 5.
                    判断完整问题属于：

                    A. 工业知识
                    B. 结构化业务数据
                    C. 普通聊天

                    Step 6.
                    如果是 A：
                    调用 knowledge_search。

                    Step 7.
                    如果是 B：
                    调用 sql_query。

                    Step 8.
                    如果是 C：
                    不调用工具。

                    Step 9.
                    工具返回结果后，再生成最终回答。

                    不要向用户暴露上述内部决策过程。
                    不要因为上一轮使用过某个工具，
                    就默认当前轮继续使用该工具。
                """
            }
        ]

        for message in history:

            messages.append(
                {
                    "role": message["role"],
                    "content": message["content"]
                }
            )

        messages.append(
            {
                "role": "user",
                "content": question
            }
        )
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        print("\n===== Agent Tool Decision =====")

        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                print(
                    "调用工具:",
                    tool_call.function.name
                )
                print(
                    "参数:",
                    tool_call.function.arguments
                )
        else:
            print("无需调用工具")

        # 没有调用工具
        if not assistant_message.tool_calls:

            return {
                "answer": assistant_message.content,
                "tool": None
            }

        # 把 Assistant 的 Tool Call 加入对话
        messages.append(
            {
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    }
                    for tool_call in assistant_message.tool_calls
                ]
            }
        )

        tool_info = None

        for tool_call in assistant_message.tool_calls:

            function_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            if function_name == "knowledge_search":

                result = knowledge_search(
                    arguments["question"]
                )

                tool_result = result["content"]

                tool_info = {
                    "name": "knowledge_search",
                    "sources": result["sources"]
                }

            elif function_name == "sql_query":

                tool_result = sql_query(
                    arguments["query"]
                )

                tool_info = {
                    "name": "sql_query",
                    "sources": []
                }

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                }
            )

        final_response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )

        return {
            "answer": final_response.choices[0].message.content,
            "tool": tool_info
        }