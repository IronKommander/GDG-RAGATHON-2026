from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
# from langchain.document_loaders import CSVLoader
from decimal import Decimal
import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "..", "dataset", "data.csv")

COLLECTION_NAME = "ST2_dataset"
SIZE=768 #for BAAI/bge-base-en-v1.5

df = pd.read_csv(file_path)
df.drop(columns=['Id'], inplace=True)
df["restaurantName"] = df["restaurantUrl"].str.split('/').str[-1]
df["distance"] = df["distance"].fillna("50")
df["distance"] = df["distance"].str.extract(r'(\d+\.\d+|\d+)').astype(float)
df.sort_values(by='distance')

print(df.head())
print(df.describe())
print(df.columns)

# Index(['restaurantName', 'isAdvertisement', 'rating', 'cuisines',
#        'deliveryTime', 'price', 'distance', 'offer', 'restaurantUrl'],
#       dtype='str')

docs = []

for _, r in df.iterrows():
    rating = r['rating'] if not pd.isna(r['rating']) else "unrated"
    price = r['price'] if not pd.isna(r['price']) else "unknown price"
    distance = r['distance'] if not pd.isna(r['distance']) else 50.0
    
    text_chunk = (
        f"{r['restaurantName']} is a restaurant located {distance}km away. "
        f"It has a rating of {rating} and offers the following cuisines: {r['cuisines']}. "
        f"The estimated delivery time is {r['deliveryTime']}"
    )
    
    metadata = {
        "restaurant_name": r['restaurantName'],
        "rating": float(r['rating']) if not pd.isna(r['rating']) else 0.0,
        "distance_km": float(r['distance']) if not pd.isna(r['distance']) else 999.9,
        "cuisines": [c.strip() for c in str(r['cuisines']).split(',')] if not pd.isna(r['cuisines']) else []
    }
    docs.append(
        Document(
            page_content=text_chunk,
            metadata=metadata
        )
    )

print(docs)
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

print("Successfully inserted into Qdrant Vector Database!")
