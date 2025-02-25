from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import re

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 

# Configure Gemini API
genai.configure(api_key="AIzaSyB8W-rt5obK0Csmf0-bDK8QcfSDQbPiYHw")

def verify_with_gemini(text):
    prompt = f"Is the following news article likely to be fake or real? Reply in the format: 'Fake - Confidence: 85%' or 'Real - Confidence: 92%'.\n\n{text}"
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    # Extract response text
    result = response.text.strip()

    # Extract 'Fake' or 'Real' & confidence using regex
    match = re.search(r"(Fake|Real) - Confidence: (\d+)%", result, re.IGNORECASE)

    if match:
        return {"status": match.group(1), "confidence": int(match.group(2))}
    
    return {"status": "Unknown", "confidence": 0}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = verify_with_gemini(text)
    print(result)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
