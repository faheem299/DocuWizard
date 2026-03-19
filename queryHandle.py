import ollama
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from config import path


#Query Handling.

def query_handler(inp:str,collection_name:str,cli:QdrantClient):
    
    #user input is embedded
    model = SentenceTransformer(path)
    query_vector = model.encode(inp).tolist()

    #using client for vector search

    results=cli.query_points(
        collection_name=f"{collection_name}",
        query=query_vector,
        limit=3
    )

    #passing similar chunks of text 
    
    specific_text = []
    for point in results.points:
        specific_text.append(point.payload["text"])
    print(specific_text)
    return specific_text