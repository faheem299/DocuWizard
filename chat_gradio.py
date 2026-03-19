import gradio as gr
from client import get_client
from pdfHandle import pdf_handler
from sentence_transformers import SentenceTransformer
from ollama import chat
from config import path
model="qwen3:4b"
from qdrant_client import QdrantClient
from queryHandle import query_handler

#chat function
def chat_response(user_input:str,collection_name:str,cli:QdrantClient):
    text = query_handler(inp=user_input,collection_name=collection_name,cli=cli)
    massege=[{
       "role":"system",
       "content":"""

       You are a document assistant.

        You will receive:
        1. Context extracted from a document
        2. A user question

        Your task:
        - Answer the question in detail in points using ONLY the provided context.
        - If the context does not contain the answer, say:
        "I could not find this information in the document."

        Rules:
        - Do not invent information.
        - Be concise and accurate.
        - Quote or summarize relevant parts of the context when useful.
        """
        },{"role":"user","content":f"context: {text},question:{user_input}"}]
    
    stream = chat(model=model,messages=massege,stream=True)
    fullresponse=""
    for chunk in stream:
            fullresponse += chunk['message']['content']
            yield fullresponse




#gradio frontend


with gr.Blocks() as demo:
    
    client_store = gr.Textbox(label='enter storage location')
    btn1 = gr.Button("entered storage location")
    client = gr.State()  

    path_manage = gr.File(file_types=['.pdf'],file_count="multiple",label='upload pdf')
    path = gr.State()
    btn2 = gr.Button("pdf embedded")
    name = gr.State()


    text = gr.State()
    question = gr.State()

    que = gr.Textbox(label='enter question')
    btn3 = gr.Button("generate answer")
    

    

    final_output = gr.Textbox(label='hehe')
    btn1.click(get_client, inputs=client_store, outputs=client)
    btn2.click(pdf_handler, inputs=[path_manage,client,path], outputs=name)
    btn3.click(chat_response,inputs=[que,name,client],outputs=final_output)

demo.queue().launch(debug=True)
