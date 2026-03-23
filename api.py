from flask import Flask
from rag_service import setup_rag, generate_response

app = Flask(__name__)

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

    response = generate_response(user_data)
    return response


@app.route('/')
def home():
    return '<h1>TEST RAG</h1>'


if __name__ == '__main__':
    app.run(debug=True, port=5004)


