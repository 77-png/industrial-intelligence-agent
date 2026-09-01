import sys
import os

sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "src"
    )
)

import streamlit as st

from agent.agent import Agent


st.set_page_config(
    page_title="Industrial Intelligence Agent",
    page_icon="🏭"
)


st.title("🏭 Industrial Intelligence Agent")

st.write(
    """
    基于 DeepSeek + RAG + Tool Calling 的工业智能助手

    支持：
    - 工业知识问答
    - 工业文档检索
    - 销售数据查询
    - 多轮对话
    """
)


@st.cache_resource
def load_agent():
    return Agent()


agent = load_agent()


if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        if message["role"] == "assistant":

            tool = message.get("tool")

            if tool:

                st.markdown(
                    f"🔧 **使用工具：** {tool['name']}"
                )

                sources = tool.get("sources", [])

                if sources:

                    st.markdown("📚 **参考来源：**")

                    for source in sources:

                        st.write(
                            f"📄 {source['source']} "
                            f"· 第 {source['page']} 页"
                        )

question = st.chat_input(
    "请输入你的问题，例如：工业数据有哪些分类？"
)

if st.button("🗑️ 清空对话"):

    st.session_state.messages = []

    st.rerun()

if question:
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "tool": result["tool"]
        }
    )

    with st.chat_message("user"):

        st.write(question)

    result = agent.run(
        question,
        history=st.session_state.messages[:-1]
    )

    with st.chat_message("assistant"):

        st.write(result["answer"])
        if result["tool"]:

            st.markdown(
                f"🔧 **使用工具：** {result['tool']['name']}"
            )

            sources = result["tool"].get(
                "sources",
                []
            )

            if sources:

                st.markdown("📚 **参考来源：**")

                for source in sources:

                    st.write(
                        f"📄 {source['source']} "
                        f"· 第 {source['page']} 页"
                    )


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "tool": result["tool"]
        }
    )
