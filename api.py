"""
API Module

Defines Flask endpoints for the Money Compass application.

Responsibilities:
- Receive requests from the frontend
- Forward user data to the RAG service
- Return generated responses

Acts as the controller layer, keeping business logic in rag_service.py.
"""

from flask import Flask
from rag_service import generate_response

app = Flask(__name__)

@app.route('/api/ai-coach', methods=['GET', 'POST'])
def ai_coach():
    """
    Generates a portfolio recommendation based on user input.

    Returns: str: AI-generated response
    """

    user_data = {
        "age": 20,
        "monthlySavings": 100,
        "investmentHorizon": "langfristig",
        "priorityReturn": 70,
        "prioritySecurity": 20,
        "priorityLiquidity": 10
    }

    # Call RAG service to generate response
    response = generate_response(user_data)
    return response


@app.route('/health')
def health():
    """
    Health check endpoint.

    Returns a simple response to verify the API is running.
    """

    return {"status": "ok"}


if __name__ == '__main__':
    app.run(debug=True, port=5004)


