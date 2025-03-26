from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
from chromadb import PersistentClient
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

app = Flask(__name__)

# Load environment variables
load_dotenv()
GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY")

if not GOOGLE_AI_API_KEY:
    raise ValueError("API key missing. Set GOOGLE_AI_API_KEY in environment variables.")

# Configure Gemini AI
genai.configure(api_key=GOOGLE_AI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# Set up ChromaDB for vector storage
DB_DIR = "./db"
os.makedirs(DB_DIR, exist_ok=True)
client = PersistentClient(path=DB_DIR)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(client=client, embedding_function=embeddings, collection_name="pregnancy_diet")


def generate_diet_plan(user_input):
    """Generate a personalized pregnancy diet plan using Gemini AI."""
    if not user_input:
        return "Invalid input. Please provide the necessary details."

    prompt = f'''
    You are an expert nutritionist specializing in pregnancy diet plans in India. 
    Create a personalized diet plan based on:
    - Trimester: {user_input.get("trimester", "Not specified")}
    - Menstrual Period: {user_input.get("menstrual_period", "Not specified")}
    - Region: {user_input.get("region", "Not specified")}
    - Diet Preference: {user_input.get("diet_preference", "Not specified")}
    - Health Issues: {user_input.get("health_issues", "None")}

    Provide a structured response with:
    1. **Meal Plan (Breakfast, Lunch, Snacks, Dinner)**
    2. **Foods for Healthy Growth** (Mother & Baby)
    3. **External Supplements**
    4. **Nutritional Benefits**
    '''

    try:
        response = model.generate_content(prompt)
        return response.text if response else "Error generating diet plan."
    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/diet-plan", methods=["POST"])
def diet_plan():
    """API endpoint to get a pregnancy diet plan."""
    try:
        user_input = request.json
        if not user_input:
            return jsonify({"error": "Request body is empty or invalid."}), 400
        
        response = generate_diet_plan(user_input)
        return jsonify({"diet_plan": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """API health check endpoint."""
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
