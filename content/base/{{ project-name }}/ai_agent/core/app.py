import os
import streamlit as st
from datetime import datetime
import openai
import pinecone
from llama_index import VectorStoreIndex, ServiceContext, StorageContext, SimpleDirectoryReader
from llama_index.llms import OpenAI
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.vector_stores import PineconeVectorStore
import logging
import nltk
import time
from ai_agent.core.create_sidebar import sidebar
import re
from ai_agent.core.config import SOLUTION_PREFIX, SEGMENTS, PINECONE_ENV, PINECONE_API_KEY, PINECONE_INDEX_METRIC
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()
print(os.environ["OPENAI_API_KEY"])
nltk.download('punkt')

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] - %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

os.environ["TOKENIZERS_PARALLELISM"] = "False"
os.environ["OPENAI_API_KEY"] = ""


st.markdown("""
    <style>
        # .reportview-container {
        #     margin-top: -2em;
        # }
        # MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        # stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

sidebar()

openai_model = st.session_state.get("model")
openai_temperature = st.session_state.get("temperature")
top_k = st.session_state.get("top_k")
persona = st.session_state.get("persona")

pinecone_index_name = f"{SOLUTION_PREFIX}-agent-{SEGMENTS[0].lower()}"


@st.cache_resource(show_spinner=False)  # Cache the data loading
def load_data():
    with st.spinner(text="Loading and indexing your data, keep it cool..."):
        logger.info('Initializing chatbot')
        time1 = datetime.now()
        pinecone_api_key = "8ac42f96-d26b-42ae-aa93-3e0d026eeb91"
        pinecone_env = "us-east-1-aws"
        embedding_model_name = "BAAI/bge-small-en-v1.5"

        logger.info(pinecone_index_name)
        logger.info(openai_model)
        logger.info(openai_temperature)
        logger.info(top_k)

        pc = Pinecone(api_key=pinecone_api_key)

        if pinecone_index_name not in pc.list_indexes().names():
            pc.create_index(
                name=pinecone_index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

        pinecone_index = pc.Index(pinecone_index_name)

        llm = OpenAI(temperature=openai_temperature, model=openai_model, max_retries=20, openai_api_key=os.getenv('OPENAI_API_KEY'))

        # construct vector store
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        # create storage context
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        if pinecone_index_name not in pc.list_indexes().names():
            documents = SimpleDirectoryReader("ai_agent/data").load_data()
            index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

        time2 = datetime.now()
        logger.info(f'Service context took:{time2 - time1}')

#         service_context = ServiceContext.from_defaults(embed_model=f"local:{embedding_model_name}", chunk_size=4096 * 2,llm=llm)

        index = VectorStoreIndex.from_vector_store(
                    vector_store=vector_store, storage_context=storage_context)

        time3 = datetime.now()
        logger.info(f'Index took:{time3 - time2}')

        retriever = index.as_retriever(
            similarity_top_k=15,
            search_type="mmr",
            search_kwargs={"mmr_threshold": 0.70, "fetch_k": 100}
        )

        query_engine = RetrieverQueryEngine.from_args(retriever, response_mode="tree_summarize")
        time4 = datetime.now()
        logger.info(f'Query Engine took:{time4 - time3}')

        return query_engine


query_engine = load_data()

if persona == SEGMENTS[0]:
    pinecone_index_name = f"{SOLUTION_PREFIX}-agent-{SEGMENTS[0].lower()}"
    logger.info(f"Selected pinecone_index_name--> {pinecone_index_name}")
    st.cache_resource.clear()
    query_engine = load_data()


def execute():
    logger.info("Inside Synthetic AI Persona Agent")

    st.title("Synthetic AI Persona Agent")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    with st.chat_message("assistant"):
        st.markdown(f"Hello, I represent the {persona} persona, How can I help")

    # Accept user input
    if prompt := st.chat_input("Ask me a question"):

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container

        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            mini_response = ""
            assistant_response = str(query_engine.query(prompt))
            logger.info(f"prompt--> {prompt}")
            logger.info(f"assistant_response-->{assistant_response}")
            regexp = re.compile(r'.*\d.*|.*-.*')

            # Simulate stream of response with milliseconds delay
            for chunk in assistant_response.splitlines():
                full_response += chunk + "\n"
                for mini_chunk in chunk.split():
                    if regexp.search(mini_chunk):
                        mini_response += mini_chunk + " "
                        time.sleep(0.05)
                    else:
                        mini_response += mini_chunk + "\n"
                        time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(mini_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = ''
    execute()