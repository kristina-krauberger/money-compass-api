from flask import Flask
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


load_dotenv()

OPENAI_API_KEY = os.getenv("SECRET_KEY_OPENAI")
QDRANT_API_KEY = os.getenv("SECRET_KEY_QDRANT")

app = Flask(__name__)

def setup_rag():
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

    # print(f"Anzahl Chunks: {len(chunks)}")
    # print("------")
    # print(chunks[0].page_content)
    # print("------")
    # print(chunks[0].metadata)

    # 3. Embeddings
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")

    # 4. Vector Store (Qdrant)
    print("Creating vector store")

    client = QdrantClient(
        url="https://ddc00627-77aa-4f63-8a67-5c90b03d15b8.europe-west3-0.gcp.cloud.qdrant.io:6333",
        api_key=QDRANT_API_KEY
    )

    rag_vectorstore = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url="https://ddc00627-77aa-4f63-8a67-5c90b03d15b8.europe-west3-0.gcp.cloud.qdrant.io:6333",
        api_key=QDRANT_API_KEY,
        collection_name="portfolio_docs"
    )
    print("Vector store created successfully")

    return rag_vectorstore

vectorstore = setup_rag()

# 5. Initialise Model
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o-mini"
)


@app.route('/api/ai-coach', methods=['GET', 'POST'])
def ai_coach():

    user_data = {
        "age": 20,
        "monthlySavings": 100,
        "investmentHorizon": "langfristig",
        "priorityReturn": 70,
        "prioritySecurity": 20,
        "priorityLiquidity": 10
    }

    # 6. Create Query with User Prompt Data
    query= f"""
    User is {user_data['age']} years old,
    saves {user_data['monthlySavings']} euros per month,
    has a {user_data['investmentHorizon']} investment horizon,
    and the following priorities:
    return {user_data['priorityReturn']}%,
    security {user_data['prioritySecurity']}%,
    liquidity {user_data['priorityLiquidity']}%.
    """

    # 7. Retrieval
    retriever = vectorstore.as_retriever()
    docs = retriever.invoke(query) # List of retrieved chunks

    # 8. Context
    context = "\n\n".join([doc.page_content for doc in docs]) # Creates coherent text out of chunks

    # 9. System Prompt
    prompt = f"""
    You are an financial coach.
    
    Use the following context to answer the question.
    
    Context: {context}
    Question: {query}
    """

    response = llm.invoke(prompt)

    return response.content


@app.route('/')
def home():
    return '<h1>TEST RAG</h1>'


if __name__ == '__main__':
    app.run(debug=True, port=5004)


