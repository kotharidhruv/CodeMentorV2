from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever
from haystack.schema import Document
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import cohere

app = Flask(__name__)
CORS(app, origins="*")

logging.basicConfig(level=logging.DEBUG)

# Initialize Haystack components
document_store = InMemoryDocumentStore(use_gpu=False, use_bm25=True)
retriever = BM25Retriever(document_store=document_store)

# Load documents from a local directory (e.g., past student code or code documentation)
def load_documents_from_directory(directory_path):
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith((".py", ".ipynb", ".txt")):  # Handle .py, .ipynb, and .txt files
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                documents.append(Document(content=content, id=filename))
    return documents

# Load documents into the document store
documents = load_documents_from_directory("C:/Users/reach/Downloads/CodeMentor-main/CodeMentor-main/RAGData")
document_store.write_documents(documents)

cohere_client = cohere.ClientV2("NKZD0sANta3S02GP5wCUYrPev7dRHW5WDbJFdbJ2")

@app.route('/api/analyze_code', methods=['POST'])
def analyze_code():
    try:
        data = request.get_json()
        code = data.get('code', '')

        if not code:
            return jsonify({"error": "No code provided"}), 400

        retrieved_docs = retriever.retrieve(query=code)
        relevant_content = " ".join([doc.content for doc in retrieved_docs])
        print(relevant_content)

        prompt = (
            f"RAG Context:\n{relevant_content}\nDo provide analysis on the above code or text. This is for your context and you can use this as reference and additional data for experience when you are analyzing the code which will be provided below.\n" \
            "You are a computer science teacher. Your task is to analyze the provided code for mistakes. Under no circumstances should you explain or rewrite the given code, provide corrected code, or suggest fixes. \n\n" \
            "Your sole focus should be:\n" \
            "- Identifying and explaining the issues in the code.\n" \
            "- Highlighting syntax errors, logical errors, and areas for improvement.\n" \
            "- Clearly stating the **exact line number(s)** where each issue exists.\n\n" \
            "**Important Instructions:**\n" \
            "- DO NOT generate or provide any code corrections, rewritten code, or solutions under any circumstances.\n" \
            "- Always reference specific line numbers for each error or problem.\n" \
            "- Use a friendly and clear tone to explain the issues and suggest ways to resolve them.\n\n" \
            f"Code:\n```Line 1 starts here:\n{code}\n```\n\n" \
            "**Final Reminder:** DO NOT generate any code corrections or solutions under any circumstances. Always include line numbers when describing the issues."
        )

        response = cohere_client.chat(
            model='command-xlarge-nightly',
            messages=[{"role": "user", "content": prompt}]
        )

        generated_text = response.message.content[0].text.strip()
        logging.debug(f"Model response: {generated_text}")

        return jsonify({"response": generated_text}), 200

    except Exception as e:
        logging.error(f"Error during code analysis: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)