"""
API Module

Defines Flask endpoints for the Money Compass application.

Responsibilities:
- Receive requests from the frontend
- Forward user data to the RAG service
- Return generated responses

Acts as the controller layer, keeping business logic in rag_service.py.
"""

import os
from flask import Flask, request, make_response
from rag_service import generate_response

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/ai-coach', methods=['GET', 'POST'])
def ai_coach():
    """
    Generates a portfolio recommendation based on user input.

    Returns: str: AI-generated response
    """
    if request.method == 'POST':
        user_data = request.get_json() or {}
    else:
        user_data = {
            "age": 60,
            "monthlySavings": 100,
            "investmentHorizon": "kurzfristig",
            "priorityReturn": 30,
            "prioritySecurity": 60,
            "priorityLiquidity": 10
        }

    # Call RAG service to generate response
    response = generate_response(user_data)
    return response


@app.route('/api/ai-coach/welcome', methods=['GET'])
def ai_coach_welcome():
    """
    Returns the welcome details and message for the coach Clara.
    """
    return {
        "name": "Clara",
        "role": "Dein Money Compass Coach",
        "avatar": "https://randomuser.me/api/portraits/women/44.jpg",
        "title": "Hey, mega, dass du startest! Bereit für deinen ersten echten Schritt? 🚀",
        "paragraph1": "In den Buddy.Fi Lektionen hast du gelernt, wie Vermögensaufbau theoretisch funktioniert. Jetzt bringen wir dieses Wissen direkt in die Praxis! Du musst kein Finanzprofi sein und brauchst keine Angst vor Fachbegriffen wie 'Asset Allocation' zu haben. Ich nehme dich einfach an die Hand.",
        "paragraph2": "Trage links deine Daten ein. Ich zeige dir ganz konkret, wie du z.B. 100 € aufteilst – wie viel in einen weltweiten ETF wie den MSCI World fließt und warum das Sinn macht. Das wird der allererste Meilenstein für deinen Sparplan!"
    }


@app.route('/health')
def health():
    """
    Health check endpoint.

    Returns a simple response to verify the API is running.
    """

    return {"status": "ok"}


if __name__ == '__main__':
    # Get port from environment variable, default to 5004 if not found
    port = int(os.environ.get('PORT', 5004))
    app.run(host='0.0.0.0', port=port)


