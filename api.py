from flask import Flask
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyMuPDFLoader

load_dotenv()

OPENAI_API_KEY = os.getenv("SECRET_KEY_OPENAI")

app = Flask(__name__)

loader = DirectoryLoader(
    path="data/",
    glob="*.pdf",
    loader_cls=PyMuPDFLoader
)

documents = loader.load()

print(f"Anzahl Dokumente: {len(documents)}")
print("------")
print(documents[0].page_content[:500])
print("------")
print(documents[0].metadata)




@app.route('/')
def home():
    return '<h1>TEST RAG</h1>'


if __name__ == '__main__':
    app.run(debug=True, port=5004)


