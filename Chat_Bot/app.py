from flask import Flask, render_template, request, jsonify
import re
import random

app = Flask(__name__)

# Define chatbot rules with multiple response options
rules = [
    (r'\b(hi|hello|hey)\b', ["Hello! How can I assist you today?", "Hi there! 😊", "Hey! What’s up?"]),
    (r'\bhow are you\b', ["I'm just a bot, but I'm here to help! How about you?", "I'm good! How about you? 😊"]),
    (r'\b(who are you|your name|what’s your name)\b', ["I am a simple rule-based chatbot.", "I'm a chatbot here to assist you!"]),
    (r'\bhelp\b', ["Sure! What do you need help with?", "I'm here to help. Ask me anything!"]),
    (r'\bbye\b', ["Goodbye! Have a great day!", "See you later! 👋"]),
    (r'\bthank you\b', ["You're welcome! I'm happy to help.", "Anytime! 😊"]),
]

def match_rule(user_input):
    """Matches user input against predefined rules."""
    for pattern, responses in rules:
        if re.search(pattern, user_input, re.IGNORECASE):
            return random.choice(responses)  # Choose a random response
    return "I'm sorry, I didn't understand that. Can you rephrase? 🤔"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.json
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"response": "Please type a message!"})
    response = match_rule(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
