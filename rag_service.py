"""
RAG Service Module

This module handles the Retrieval-Augmented Generation (RAG) pipeline for the Money Compass application.

Responsibilities:
- Load and process financial knowledge documents (PDFs)
- Split documents into chunks for embedding
- Create and store embeddings in a Qdrant vector database
- Retrieve relevant document chunks based on user input
- Build prompts using retrieved context and user data
- Generate responses using an LLM (OpenAI)

Usage:
Called by api.py to generate AI-based portfolio explanations.

This module acts as the core AI logic layer, separating business logic and API handling from AI processing.
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore


load_dotenv()

QDRANT_API_KEY = os.getenv("SECRET_KEY_QDRANT")
OPENAI_API_KEY = os.getenv("SECRET_KEY_OPENAI")


def setup_rag():
    """
    Sets up the Retrieval-Augmented Generation (RAG) pipeline.

    Steps:
    1. Load PDF documents from the data folder
    2. Split documents into smaller chunks for processing
    3. Convert text chunks into embeddings (vector representation)
    4. Store embeddings in a Qdrant vector database

    Returns:
        QdrantVectorStore: A vector store containing all embedded document chunks
    """

    # Step 1: Load documents from PDF files
    # DirectoryLoader scans the folder and uses PyMuPDFLoader to extract text from each PDF
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

    # Step 2: Split documents into smaller chunks
    # This improves retrieval accuracy because smaller chunks are easier to match semantically
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    # print(f"Anzahl Chunks: {len(chunks)}")
    # print("------")
    # print(chunks[0].page_content)
    # print("------")
    # print(chunks[0].metadata)

    # Step 3: Convert text chunks into embeddings
    # Each chunk is transformed into a vector (numerical representation) for similarity search
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-3-small")

    # Step 4: Store embeddings in Qdrant vector database
    # Qdrant stores vectors and allows efficient similarity search during retrieval
    print("Creating vector store")
    rag_vectorstore = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url="https://2ae93c26-c736-43f9-b09d-6dffe60ad4c1.eu-central-1-0.aws.cloud.qdrant.io",
        api_key=QDRANT_API_KEY,
        collection_name="portfolio_docs"
    )
    print("Vector store created successfully")

    return rag_vectorstore


vectorstore = setup_rag() # Vector store (init once): loads and indexes documents
retriever = vectorstore.as_retriever()  # Retriever: semantic search over the vector store

# LLM (init once): generates the final answer from the prompt
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o-mini",
    temperature=0.1
)


def load_prompt():
    """
    Load system prompt from file.

    Returns:
        str: Prompt text
    """

    with open("prompts/system_prompt.txt") as f:
        return f.read()


def generate_response(user_data):
    """
    Generate an AI response based on user data using the RAG pipeline.

    Steps:
    1. Build query from structured user input
    2. Retrieve relevant document chunks
    3. Combine chunks into a context
    4. Build final prompt (system prompt + context + query)
    5. Generate response using LLM

    Args:
        user_data (dict): User input from frontend

    Returns:
        str: Generated response text
    """

    # Step 1: Build query from user input
    query = f"""
    User is {user_data['age']} years old,
    saves {user_data['monthlySavings']} euros per month,
    has a {user_data['investmentHorizon']} investment horizon,
    and the following priorities:
    return {user_data['priorityReturn']}%,
    security {user_data['prioritySecurity']}%,
    liquidity {user_data['priorityLiquidity']}%.
    """

    # Step 2: Retrieve relevant document chunks
    docs = retriever.invoke(query)  # List of retrieved chunks

    # Step 3: Build context for the LLM
    context = "\n\n".join([doc.page_content for doc in docs])  # Creates coherent text out of chunks

    # Step 4: Build final prompt
    system_prompt = load_prompt()
    prompt = f"""
    {system_prompt}

    Context: 
    {context}
    
    User profile:
    {query}
    """

    # Step 5: Generate response with LLM
    response = llm.invoke(prompt)
    return response.content