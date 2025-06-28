import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import smtplib

load_dotenv()

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/generate-email', methods=['POST'])
def generate_email():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "You are a proffesional email creater gives only email body as response with no subject"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3-70b-8192",
            temperature=0.7,
            max_tokens=1024
        )
        return jsonify({"email": chat_completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error generate email": str(e)}), 500

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    recipient = data['recipient']
    email_body = data['email']
    sender = "aayushsingh692002@gmail.com"
    password = os.environ.get("GMAILPASS")
    subject = data['subject']
    text = f"Subject:{subject}\n\n{email_body}"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, recipient, text)
    return jsonify({"message": "Email sent successfully"}), 200
    

if __name__ == '__main__':
    app.run(port=5000)