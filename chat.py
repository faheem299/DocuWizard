from ollama import chat
from queryHandle import query_handler
from pdfHandle import pdf_handler
from client import get_client
model="llama3.1:8b"

#Terminal version. Works with larger models because gradio is not taking up RAM.

print("path for storage: ")
store = input()
client = get_client(store)
while True:
    

    print("input path to pdf: ")
    path = input().split(',')
    if not path:
        break
    if path == "bye":
        messege.clear()
        break

    name = pdf_handler(cli=client,path_array=path)
    while True:

        user_input = input()
        if not user_input:
            break
        if user_input == "bye":
            messege.clear()
            break
        text = query_handler(inp=user_input,cli=client,collection_name=name)
        
        messege=[{
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
        stream = chat(model,messege,stream=True)
        answer = ""
        for chunk in stream:
            content = chunk['message']['content']
            print(content, end="", flush=True)
            answer += content
        print()
    

