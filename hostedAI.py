from flask import Flask, request, jsonify
from online_ai import GeminiChatbot

app = Flask(__name__)
chatbot = GeminiChatbot()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    input_text = data.get('input_text', '')
    response = chatbot.get_gemini_response(input_text)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
