# 🏭 Industrial Intelligence Agent

An industrial intelligence assistant built with **DeepSeek + RAG + Tool Calling**, supporting industrial knowledge retrieval, structured data querying, multi-turn conversation, and context-aware tool routing.

## 📌 Overview

Industrial Intelligence Agent is a lightweight LLM Agent prototype designed for industrial knowledge Q&A and business data analysis.

The system combines:

* **Large Language Model reasoning**
* **Retrieval-Augmented Generation (RAG)**
* **Vector database retrieval**
* **SQL structured data querying**
* **Function / Tool Calling**
* **Multi-turn context understanding**
* **Streamlit conversational interface**

The Agent dynamically selects the appropriate tool according to the user's current intent rather than relying only on keyword matching or the tool used in the previous turn.

---

## ✨ Features

### 🔎 Industrial Knowledge RAG

The Agent can retrieve relevant information from industrial documents and answer questions such as:

* What are the main categories of industrial data?
* What is an industrial internet platform?
* How is industrial data classified and graded?
* What do industrial standards and guidelines specify?

The RAG pipeline uses semantic retrieval to search the industrial knowledge base before generating the final answer.

### 🗄️ Structured Data Query

For numerical and business-related questions, the Agent can automatically call the SQL query tool.

Example questions:

* Which product had the highest sales in 2026?
* What was the total sales amount in 2026?
* How many records are stored in the database?
* What is the sales ranking of different products?

The structured demo database is implemented with SQLite.

### 🔧 Automatic Tool Calling

The Agent currently supports two tools:

| Tool               | Description                                               |
| ------------------ | --------------------------------------------------------- |
| `knowledge_search` | Retrieve industrial knowledge from the RAG knowledge base |
| `sql_query`        | Query structured business data from the SQLite database   |

DeepSeek determines whether a tool is required and selects the appropriate tool according to user intent.

### 🧠 Multi-turn Context Understanding

The system supports contextual follow-up questions.

Example:

```text
User:
Which product had the highest sales in 2026?

Agent:
Industrial Software Platform.

Tool:
sql_query
```

Follow-up:

```text
User:
What was its sales amount?

Agent:
350000.

Tool:
sql_query
```

The Agent resolves the pronoun **"its"** using conversation history.

### 🔀 Context-aware Cross-tool Routing

The Agent can also switch tools during a multi-turn conversation.

Example:

```text
User:
Which product had the highest sales in 2026?

→ sql_query

User:
What was its sales amount?

→ sql_query

User:
Which category of industrial data does it belong to?

→ knowledge_search
```

Although the entity originally comes from the SQL database, the final question is an industrial knowledge question.

Therefore, the Agent re-evaluates the **current intent** and switches from the SQL tool to the RAG tool.

This prevents the system from mechanically continuing to use the tool selected in the previous turn.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │        User         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Streamlit Chat    │
                    │   Multi-turn UI     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    DeepSeek Agent   │
                    │ Context Understanding│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Tool Routing     │
                    └─────────┬─┬─────────┘
                              │ │
                    ┌─────────┘ └─────────┐
                    ▼                     ▼
          ┌──────────────────┐   ┌──────────────────┐
          │ knowledge_search │   │    sql_query     │
          └────────┬─────────┘   └────────┬─────────┘
                   │                      │
                   ▼                      ▼
          ┌──────────────────┐   ┌──────────────────┐
          │    BGE-M3        │   │      SQLite      │
          │   Embedding      │   │  Business Data   │
          └────────┬─────────┘   └──────────────────┘
                   │
                   ▼
          ┌──────────────────┐
          │     Chroma       │
          │ Vector Database  │
          └────────┬─────────┘
                   │
                   ▼
          ┌──────────────────┐
          │ Industrial PDFs  │
          └──────────────────┘
```

---

## 🛠️ Tech Stack

### LLM

* DeepSeek API
* `deepseek-chat`

### Agent

* Function Calling / Tool Calling
* Context-aware tool routing
* Multi-turn conversation history

### RAG

* BGE-M3 Embedding
* Chroma Vector Database
* Industrial PDF documents
* Semantic retrieval

### Structured Data

* SQLite
* SQL query tool

### Application

* Python
* Streamlit

---

## 📂 Project Structure

```text
AI-RAG-Agent/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── data/
│   ├── documents/
│   ├── chroma/
│   └── demo.db
│
└── src/
    ├── agent/
    │   └── agent.py
    │
    ├── llm/
    │
    ├── rag/
    │
    └── tools/
        ├── knowledge_tool.py
        └── sql_tool.py
```

> `.env`, local vector database files, and local database files are excluded from Git through `.gitignore`.

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/77-png/industrial-intelligence-agent.git
cd industrial-intelligence-agent
```

### 2. Create a virtual environment

Using Conda:

```bash
conda create -n ai-rag-agent python=3.10
conda activate ai-rag-agent
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
```

Do **not** commit the `.env` file to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

Then open the Streamlit page in your browser.

---

## 💬 Example Usage

### Industrial Knowledge Query

```text
User:
工业数据有哪些主要分类？

Agent:
[Answer generated based on retrieved industrial documents]

Tool:
knowledge_search
```

The interface also displays the retrieved document sources.

### Structured Data Query

```text
User:
2026年销售额最高的产品是什么？

Agent:
工业软件平台，销售额为 350000。

Tool:
sql_query
```

### Multi-turn Query

```text
User:
2026年销售额最高的产品是什么？

Agent:
工业软件平台。

User:
它的销售额是多少？

Agent:
350000。
```

### Cross-tool Query

```text
User:
2026年销售额最高的产品是什么？

→ sql_query

User:
它属于哪类工业数据？

→ knowledge_search
```

---

## 🧩 Agent Decision Logic

For every user query, the Agent performs the following high-level process:

```text
Current User Query
        │
        ▼
Read Conversation History
        │
        ▼
Resolve Pronouns / Missing Context
        │
        ▼
Understand Current User Intent
        │
        ▼
Classify Query
   ┌────┼────┐
   │    │    │
   ▼    ▼    ▼
Knowledge SQL Casual Chat
   │    │
   ▼    ▼
 RAG   SQL
 Tool  Tool
   │    │
   └──┬─┘
      ▼
Generate Final Response
```

Tool selection is based on the **semantic intent of the current complete question**, rather than simply inheriting the tool used in the previous conversation turn.

---

## 🔐 Security

Sensitive information is stored through environment variables.

The following files should not be committed:

```text
.env
data/chroma/
data/*.db
.streamlit/secrets.toml
```

An example environment configuration can be provided through `.env.example`.

---

## 📈 Future Improvements

Potential extensions include:

* Conversation memory compression for long sessions
* Retrieval-based long-term memory
* More industrial business tools
* SQL query validation and stronger security restrictions
* Hybrid retrieval
* Reranking
* RAG evaluation
* Agent observability and tracing
* More structured industrial datasets
* Deployment to a public cloud environment

---

## 🎯 Project Highlights

This project focuses on three practical LLM application problems:

1. **How to combine unstructured industrial knowledge with structured business data**
2. **How an Agent dynamically selects between RAG and SQL tools**
3. **How multi-turn context affects tool routing and user intent understanding**

Instead of building a single RAG chatbot, the system integrates retrieval, structured querying, multi-turn context understanding, and dynamic Tool Calling into one lightweight industrial intelligence Agent.
