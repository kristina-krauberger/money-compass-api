# Money Compass Service API

Backend service for the Money Compass AI Investment Recommendation System.

This API is responsible for handling user input, processing recommendation logic, and generating AI-based responses using LLMs and RAG-style context.

---

## Overview

The Money Compass Service API acts as the backend layer of the system.

It connects:

- user input from the frontend  
- decision logic (prompt-based)  
- LLM-generated responses  
- RAG-style context (portfolio documents)  

The goal is to return a simple, human-friendly investment recommendation.

---

## Current Status

In development  

Current state:

- basic Flask app setup  
- environment configuration  
- initial API structure (WIP)  

Planned:

- recommendation endpoint (`/api/money-compass`)  
- prompt-based decision logic  
- integration with LLM API  
- RAG-style context retrieval  

---

## Tech Stack

Python  
Flask  
dotenv  

Planned:

LLM API (OpenAI or similar)  
Prompt Engineering  
RAG (context-based retrieval)

---

## Project Structure

```bash
.
├── api.py
├── .env
└── TBD