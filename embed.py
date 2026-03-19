import gc
from sentence_transformers import SentenceTransformer
from config import path
model = SentenceTransformer(path)

#chunks of data are passed and embeddings are returned

def embed(c):
 
    embed = model.encode(c,normalize_embeddings=True)

    data_point = []
    for i,emb in enumerate(embed):
        data_point.append(
            {"id":i,
            "text":c[i],
            "embedding":emb.tolist()})
    print("completed embedding...")
    
    #clearing RAM for memory efficiency

    del embed
    gc.collect()
    return data_point