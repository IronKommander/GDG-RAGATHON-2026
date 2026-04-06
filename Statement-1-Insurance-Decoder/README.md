# ST-1 Insurance Decoder
This is our implementation of the first problem statement.

## Installation
Ensure that Qdrant is up and running:
Bash
```
docker run -p 6333:6333 qdrant/qdrant
```

## Architecture
1. LangGraph as the orchestration framework.
2. Qdrant as local vector database.
3. BAAI General Embedding(Base) as the embedding model.
4. BAAI General Embedding(Base) as the reranker model.
5. Cohere Command R as the base LLM model.
6. FastAPI for making endpoints for the frontend.

## Tech Stack

## Bonus Attempts
