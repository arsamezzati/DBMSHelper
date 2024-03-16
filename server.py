from flask import Flask, request, jsonify
import anthropic

app = Flask(__name__)
API_KEY = "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"  # Replace with your actual API key
client = anthropic.Anthropic(api_key=API_KEY)


@app.route('/send_request', methods=['POST'])
def send_request():
    try:
        # gets json data (handles incoming request)
        data = request.json
        print(data)

        # Extract user message from request
        user_message = data['text']  # Ensure this aligns with your client's JSON structure

        systemPrompt = "Write the query for " + data['dbms'] + "database with " + data["lang"] + " programming language and with proper code embedding, do not explain anything show only code and properly embedded"

        print(user_message)

        # Use the Anthropic package to create a message
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            system=systemPrompt,
            messages=[{"role": "user", "content": user_message}]
        )

        print(response.content)

        # Extract the text content from the response
        response_text = response.content[0].text

        # Return the response as JSON
        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, port=8000)