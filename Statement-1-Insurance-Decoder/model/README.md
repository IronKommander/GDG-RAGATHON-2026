# ST-1 Insurance Decoder
This is our implementation of the first problem statement.

## Installation
1. Setup your virtual environment using ```python venv``` or ```uv```.
2. Ensure that Qdrant is up and running locally on port 6333:
Bash
```
docker run -p 6333:6333 qdrant/qdrant
```


## Architecture
1. LangGraph as the orchestration framework.
2. Qdrant as local vector database.
3. BAAI General Embedding(Base) as the embedding model.
5. llama-3.3-70b-versatile as the base LLM model.
6. FastAPI for making endpoints for the frontend.

## Bonus Attempts
Our bot explicitly cites the Section and Clause number through two major implementations:
1. Chunking using MarkdownHeaderTextSplitter, retaining the metadata of Section and Clause headers.
2. Using Pydantic classes so that the model always gives output with Section and Clause headers.
