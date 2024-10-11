import streamlit as st
import base64

from ai_agent.core.config import SEGMENTS

MODEL_LIST = ["gpt-3.5-turbo", "gpt-4"]
PERSONA_LIST = SEGMENTS


def sidebar():
    with st.sidebar:
        with open("ai_agent/core/p6m-Logotype-Black-VOS.png", "rb") as f:
            # with open("p6m-Logotype-Black-VOS.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")

            st.sidebar.markdown(
                f"""
                <div style="display:table;margin-top:-30%;margin-left:00%;">
                    <img src="data:image/png;base64,{data}" width="150" height="60">
                </div>
                """,
                unsafe_allow_html=True,
            )

        persona: str = st.selectbox("Synthetic Persona", options=PERSONA_LIST)  # type: ignore
        model: str = st.selectbox("Model", options=MODEL_LIST)  # type: ignore
        temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.5, step=0.01)
        top_k = st.sidebar.slider('top_k', min_value=1, max_value=50, value=15, step=1)

        st.session_state["persona"] = persona
        st.session_state["model"] = model
        st.session_state["temperature"] = temperature
        st.session_state["top_k"] = top_k

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "Synthetic Personas allows you to ask questions about your "
            "documents and enable AI Smoke Tests "
        )
        st.markdown(
            "You can reach out to "
            "[AIML Team](https://www.notion.so/p6m/AIML-Team-Wiki-c68b771fe3d047559cf7111efb7218bc?pvs=4)"
            " with your feedback and suggestions💡"
        )
        st.markdown("---")
