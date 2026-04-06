from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "..", "docs", "TITANSECURE.pdf")
loader = PyPDFLoader(file_path=file_path)
docs = loader.load()

COLLECTION_NAME = "ST1_docs"
SIZE=768 #for BAAI/bge-base-en-v1.5

splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=30,  # ~20% overlap, since document is technical
    separators=["\n\n", "\n", ". ", " ", ""])
chunks = splitter.split_documents(docs)

bge_embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5", #Using the base BGE embedding model
    model_kwargs={"device":"cpu"},
    encode_kwargs={"normalize_embeddings": True},
    query_encode_kwargs={"prompt": "Represent this sentence for searching relevant passages: "}
)

qdrant_db = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=bge_embeddings,
    url="http://localhost:6333",
    collection_name=COLLECTION_NAME
)
