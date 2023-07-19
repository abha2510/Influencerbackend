# from flask import Flask, request, jsonify
# import openai
# from flask_cors import CORS
# import re
# from langdetect import detect

# app = Flask(__name__)
# CORS(app)
# openai.api_key = "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"

# chat_history = []

# @app.route("/getChatbotResponse", methods=["POST"])
# def get_chatbot_response():
#     user_input = request.json.get("user_input", "")

#     # Define the regular expression pattern to match the specific scenario
#     pattern = r"(Hi Harpreet, I randomly came across your profile today).*?(speaking my mind\.)"

#     # Check if the user input matches the pattern using re.search()
#     match = re.search(pattern, user_input)

#     if match:
#         # If the pattern is matched, create a dynamic response based on the match
#         response_text = "Thank you for your kind words. I'm glad you " + match.group(2) + " Best wishes to you!"

#     else:
#         # Use OpenAI GPT-3.5 for general user inputs
#         messages = [
#             {"role": "system", "content": "You are a helpful assistant that speaks English."},
#             {"role": "user", "content": user_input}
#         ]

#         if chat_history:
#             messages.append({"role": "assistant", "content": chat_history[-1]})

#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=messages,
#             temperature=1.05,
#             max_tokens=202,
#             top_p=1,
#             frequency_penalty=0,
#             presence_penalty=0
#         )

#         chatbot_response = response["choices"][0]["message"]["content"]

#         # Filter out incomplete sentences
#         sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', chatbot_response)
#         complete_sentences = [sentence for sentence in sentences if len(sentence) > 200]

#         if complete_sentences:
#             chat_history.append(complete_sentences[-1])
#             response_text = complete_sentences[-1]
#         else:
#             chat_history.append(chatbot_response)
#             response_text = chatbot_response

#     return jsonify({"chatbot_response": response_text})




# if __name__ == "__main__":
#     app.run(debug=True)

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

    # Define the regular expression pattern to match the specific scenario
    pattern = r"(Hi Harpreet, I randomly came across your profile today).*?(speaking my mind\.)"

    # Check if the user input matches the pattern using re.search()
    match = re.search(pattern, user_input)

    if match:
        # If the pattern is matched, create a dynamic response based on the match
        response_text = "Thank you for your kind words. I'm glad you " + match.group(2) + " Best wishes to you!"
    else:
        # Use OpenAI GPT-3.5 for general user inputs
        messages = [
            {"role": "system", "content": "You are a helpful assistant that speaks the same language as the user."},
            {"role": "user", "content": user_input}
        ]

        if chat_history:
            messages.append({"role": "assistant", "content": chat_history[-1]})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=1.05,
            max_tokens=80,
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
            response_text = complete_sentences[-1]
        else:
            chat_history.append(chatbot_response)
            response_text = chatbot_response

    return jsonify({"chatbot_response": response_text})


if __name__ == "__main__":
    app.run(debug=True)
