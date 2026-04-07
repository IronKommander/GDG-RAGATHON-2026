from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.tools import tool
from langchain.chat_models import init_chat_model

bge_embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5", #Using the base BGE embedding model
    model_kwargs={"device":"cpu"},
    encode_kwargs={"normalize_embeddings": True},
    query_encode_kwargs={"prompt": "Represent this sentence for searching relevant passages: "}
)

COLLECTION_NAME = "ST1_docs"
vectorstore = QdrantVectorStore.from_existing_collection(
    collection_name=COLLECTION_NAME,
    embedding=bge_embeddings
)
retriever = vectorstore.as_retriever()

@tool
def retrieve_blog_posts(query: str) -> str:
    """Search and return info about TITAN SECURE's Universal Health & Wellness Policy."""
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])

tools = [retrieve_blog_posts]

llm = init_chat_model(
    "cohere/command-r",
    model_provider="cohere",
    temperature=0.7
)
