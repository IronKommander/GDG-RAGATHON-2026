from langchain_text_splitters import RecursiveCharacterTextSplitter, markdown
from langchain_huggingface import HuggingFaceEmbeddings
import pymupdf4llm
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_qdrant import QdrantVectorStore
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "..", "docs", "TITANSECURE.pdf")

COLLECTION_NAME = "ST1_docs"
SIZE=768 #for BAAI/bge-base-en-v1.5

md_txt = pymupdf4llm.to_markdown(file_path)
headers = [
    ("#", "Section"),
    ("##", "Clause"),
    ("###", "Sub-clause")
]

md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers)
docs = md_splitter.split_text(md_txt)

bge_embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en-v1.5", #Using the base BGE embedding model
    model_kwargs={"device":"cpu"},
    encode_kwargs={"normalize_embeddings": True},
    query_encode_kwargs={"prompt": "Represent this sentence for searching relevant passages: "}
)

qdrant_db = QdrantVectorStore.from_documents(
    documents=docs,
    embedding=bge_embeddings,
    url="http://localhost:6333",
    collection_name=COLLECTION_NAME,
    force_recreate = True
)
