from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("SECRET_KEY_OPENAI")

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>TEST RAG</h1>'


if __name__ == '__main__':
    app.run(debug=True, port=5004)