from llama_index.core import Document
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import path

#Semantic splitter function where the hugginFace model is used for chunking based on similarity

def semantic_splitter(t:str):
    doc = Document(text=t)
    semantic_splitter = SemanticSplitterNodeParser(
        buffer_size=1,
        breakpoint_percentile_threshold=95,
        embed_model=HuggingFaceEmbedding(model_name=path)
    )
    nodes = semantic_splitter.get_nodes_from_documents([doc])
    print(f"divided into {len(nodes)} chunks")
    return [n.text for n in nodes]



