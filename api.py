from flask import Flask
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

OPENAI_API_KEY = os.getenv("SECRET_KEY_OPENAI")

app = Flask(__name__)

# 1. Load with DirectoryLoader and PyMuPDF
loader = DirectoryLoader(
    path="data/",
    glob="*.pdf",
    loader_cls=PyMuPDFLoader
)

documents = loader.load()

# print(f"Anzahl Dokumente: {len(documents)}")
# print("------")
# print(documents[0].page_content[:500])
# print("------")
# print(documents[0].metadata)

# 2. Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

print(f"Anzahl Chunks: {len(chunks)}")
print("------")
print(chunks[0].page_content)
print("------")
print(chunks[0].metadata)


@app.route('/')
def home():
    return '<h1>TEST RAG</h1>'


if __name__ == '__main__':
    app.run(debug=True, port=5004)


