from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)
openai.api_key = "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"

chat_history = []

@app.route("/getChatbotResponse", methods=["POST"])
def get_chatbot_response():
    user_input = request.json.get("user_input", "")
    messages = [
        {"role": "user", "content": user_input}
    ]

    if chat_history:
        messages.append({"role": "assistant", "content": chat_history[-1]})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=1.05,
        max_tokens=202,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    chatbot_response = response["choices"][0]["message"]["content"]
    
    # Filter out incomplete sentences
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', chatbot_response)
    complete_sentences = [sentence for sentence in sentences if len(sentence) > 200]

    if complete_sentences:
        chat_history.append(complete_sentences[-1])
        return jsonify({"chatbot_response": complete_sentences[-1]})
    else:
        chat_history.append(chatbot_response)
        return jsonify({"chatbot_response": chatbot_response})
if __name__ == "__main__":
    app.run(debug=True)

