from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import requests
import cohere

app = Flask(__name__)

CORS(app, origins="https://astounding-dolphin-78cd47.netlify.app", supports_credentials=True)

logging.basicConfig(level=logging.DEBUG)

# Initialize the Cohere client
cohere_client = cohere.Client("NKZD0sANta3S02GP5wCUYrPev7dRHW5WDbJFdbJ2")

@app.route('/api/analyze_code', methods=['POST', 'OPTIONS'])
def analyze_code():
    if request.method == 'OPTIONS':
        return '', 200
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            code = data.get('code', '')

            if not code:
                return jsonify({"error": "No code provided"}), 400

            prompt = (
                "You are a computer science teacher. Your task is to analyze the provided code for mistakes. Under no circumstances should you explain or rewrite the given code, provide corrected code, or suggest fixes. \n\n" 
                "Your sole focus should be:\n" 
                "- Identifying and explaining the issues in the code.\n" 
                "- Highlighting syntax errors, logical errors, and areas for improvement.\n" 
                "- Clearly stating the **exact line number(s)** where each issue exists.\n\n" 
                "**Important Instructions:**\n" 
                "- DO NOT generate or provide any code corrections, rewritten code, or solutions under any circumstances.\n" 
                "- Always reference specific line numbers for each error or problem.\n" 
                "- Use a friendly and clear tone to explain the issues and suggest ways to resolve them.\n\n" 
                f"Code:\n```Line 1 starts here:\n{code}\n```\n\n" 
                "**Final Reminder:** DO NOT generate any code corrections or solutions under any circumstances. Always include line numbers when describing the issues."
            )

            # Call Cohere API to analyze the code with chat history (if any previous context is required)
            chat_history = [
                {"role": "user", "message": "I am submitting some code for analysis."},
                {"role": "chatbot", "message": "Sure! Please provide the code."}
            ]

            response = cohere_client.chat(
                chat_history=chat_history,
                message=prompt,
                connectors=[{"id": "web-search"}]  # Example of using connectors if needed
            )

            # Access the content of the response correctly
            generated_text = response.messages[0].text.strip()  # Use 'messages' and 'text' attributes

            logging.debug(f"Model response: {generated_text}")

            return jsonify({"response": generated_text}), 200

        except Exception as e:
            logging.error(f"Error during code analysis: {str(e)}")
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
