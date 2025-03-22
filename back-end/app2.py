from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import logging
import os
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever  # Use BM25Retriever as ElasticsearchRetriever might be deprecated or moved
from haystack.schema import Document
import cohere

# Set the correct path to the React build folder
app = Flask(__name__, static_folder="../flask_project/build", static_url_path="/")
CORS(app, origins="*")

logging.basicConfig(level=logging.DEBUG)

# Initialize Haystack components
document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")
retriever = BM25Retriever(document_store=document_store)  # Update based on the latest retriever available

# Load documents from a local directory
def load_documents_from_directory(directory_path):
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith((".py", ".ipynb", ".txt")):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                documents.append(Document(content=content, id=filename))
    return documents

documents = load_documents_from_directory("RAGData")
document_store.write_documents(documents)

cohere_client = cohere.Client("NKZD0sANta3S02GP5wCUYrPev7dRHW5WDbJFdbJ2")  # Ensure usage of the correct Client

# Serve React's index.html for the root route
@app.route('/')
def serve_react():
    return send_from_directory(app.static_folder, "index.html")

# Serve other static files like JS, CSS, images
@app.route('/<path:path>')
def serve_static_files(path):
    # Ensure React routes fallback to index.html
    try:
        return send_from_directory(app.static_folder, path)
    except Exception:
        return send_from_directory(app.static_folder, "index.html")

# Flask API endpoint to analyze code
@app.route('/api/analyze_code', methods=['POST'])
def analyze_code():
    try:
        data = request.get_json()
        code = data.get('code', '')

        if not code:
            return jsonify({"error": "No code provided"}), 400

        retrieved_docs = retriever.retrieve(query=code)
        relevant_content = " ".join([doc.content for doc in retrieved_docs])

        prompt = (f"RAG Context:\n{relevant_content}\nAnalyze the provided code:")

        response = cohere_client.chat(
            model='command-xlarge-nightly',
            messages=[{"role": "user", "content": prompt}]
        )

        generated_text = response.message.content.strip()  # Ensure correct extraction of generated text
        logging.debug(f"Model response: {generated_text}")

        return jsonify({"response": generated_text}), 200

    except Exception as e:
        logging.error(f"Error during code analysis: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
