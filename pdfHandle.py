from pdf_to_text import pdfToText
from text_to_chunk import semantic_splitter
from embed import embed
from client import get_client
from collection import custom_collection
from qdrant_client import QdrantClient
import os
import shutil

#combining and simplifying all PDF handling functions into one function.

def pdf_handler(files,cli:QdrantClient,path_array):

    if not files:
        return "no files uploaded"
    save_dir = "uploaded_pdfs"
    os.makedirs(save_dir,exist_ok=True)

    new_paths=[]
    for f in files:
        filename = os.path.basename(f.name)
        dest = os.path.join(save_dir,filename)
        shutil.copy(f.name,dest)
        new_paths.append(dest)
    print(new_paths)
    path_array=new_paths
    collection_list = cli.get_collections().collections
    collection_names = [c.name for c in collection_list]

    name=""

    for path in path_array:

        base_name = os.path.basename(path)
        temp_name = os.path.splitext(base_name)[0]
        name+=temp_name
    
    if name not in collection_names:
                total_text=""
                for path in path_array:
                    text = pdfToText(path)
                    total_text+=text

                chunks = semantic_splitter(total_text)
                embed_data = embed(chunks)


                custom_collection(cli,name,embed_data)
                print(name)
                return name
    else:
        print("already there")
        return name