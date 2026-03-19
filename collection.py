from qdrant_client import models,QdrantClient

#Vector embeddings are converted to Pointstructs for qdrant database
def storing_data(dat):
    points = []
    for d in dat:
        points.append(
            models.PointStruct(
                id=d["id"],
                vector=d["embedding"],
                payload={"text":d["text"]}
            )
        )
    return points


def custom_collection(client:QdrantClient,name:str,dat):

    #Passing vector embeddings to the database ONLY IF it isnt stored there before

    collection_list = client.get_collections().collections
    collection_names = [c.name for c in collection_list]

    if name not in collection_names:
        client.create_collection(
            collection_name=f"{name}",
            vectors_config=models.VectorParams(
            size=len(dat[0]["embedding"]),
            distance=models.Distance.COSINE
        ))

        points = storing_data(dat)
        client.upsert(
        collection_name=f"{name}",
        points=points)
        print("stored successfully!")
    else:
        print("previously there")