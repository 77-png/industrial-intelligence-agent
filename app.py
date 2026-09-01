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

st.caption(
    "基于 DeepSeek + RAG + Tool Calling 的工业智能助手"
)


# =========================
# 加载 Agent
# =========================

@st.cache_resource
def load_agent():
    return Agent()


agent = load_agent()


# =========================
# 侧边栏
# =========================

with st.sidebar:

    st.header("⚙️ Agent 控制台")

    st.markdown(
        """
        **支持能力**

        🔎 工业知识 RAG 检索  
        🗄️ SQL 数据查询  
        🧠 多轮上下文理解  
        🔧 自动 Tool Calling
        """
    )

    if st.button(
        "🗑️ 清空对话",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# =========================
# 初始化历史
# =========================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================
# 显示历史消息
# =========================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        # Assistant 消息显示工具信息
        if (
            message["role"] == "assistant"
            and message.get("tool")
        ):

            tool = message["tool"]

            st.caption(
                f"🔧 Tool · {tool['name']}"
            )

            sources = tool.get(
                "sources",
                []
            )

            if sources:

                with st.expander(
                    "📚 查看参考来源"
                ):

                    for source in sources:

                        st.write(
                            f"📄 {source['source']} "
                            f"· 第 {source['page']} 页"
                        )


# =========================
# Chat 输入框
# =========================

question = st.chat_input(
    "询问工业知识或业务数据..."
)


if question:

    # =====================
    # 显示当前用户问题
    # =====================

    with st.chat_message("user"):

        st.markdown(question)


    # =====================
    # 构造历史
    # =====================

    history = []

    for message in st.session_state.messages:

        history.append(
            {
                "role": message["role"],
                "content": message["content"]
            }
        )


    # =====================
    # 调用 Agent
    # =====================

    with st.chat_message("assistant"):

        with st.spinner(
            "正在分析问题..."
        ):

            result = agent.run(
                question,
                history=history
            )


        st.markdown(
            result["answer"]
        )


        # =================
        # 工具调用信息
        # =================

        if result["tool"]:

            tool = result["tool"]

            st.caption(
                f"🔧 Tool · {tool['name']}"
            )

            sources = tool.get(
                "sources",
                []
            )

            if sources:

                with st.expander(
                    "📚 查看参考来源"
                ):

                    for source in sources:

                        st.write(
                            f"📄 {source['source']} "
                            f"· 第 {source['page']} 页"
                        )


    # =====================
    # 保存用户消息
    # =====================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # =====================
    # 保存 Assistant 消息
    # =====================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["answer"],
            "tool": result["tool"]
        }
    )