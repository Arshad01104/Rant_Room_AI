import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# 👉 Home route to render index.html
@app.route("/")
def home():
    return render_template("index.html")

# 👉 Rant API route
@app.route("/rant", methods=["POST"])
def rant():
    data = request.get_json()
    rant = data.get("rant", "")
    tone = data.get("tone", "funny")

    prompt = f"""
You're Rant Room AI – reply to the user's rant with a {tone} tone.
Here's the rant:
{rant}

Respond in 1-9 sentences, add emoji if it fits the mood.
 Only in school teacher you can give the answer of all question and behave like an ideal teacher.
 and give the answer of complex calculations but you treat user as a student and never scold them and 
 in reporter you are able to give all the current news about the topic and you never say that you are an AI
"""

    try:
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text.strip()})
    except Exception as e:
        return jsonify({"reply": f"Gemini API error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)