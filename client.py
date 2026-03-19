from qdrant_client import QdrantClient
#creating a client function

def get_client(p:str):
    cli = QdrantClient(path=p)
    print("client created...")
    return cli

