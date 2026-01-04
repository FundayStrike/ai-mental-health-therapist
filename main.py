from flask import Flask, render_template, request
from google import genai
from google.genai.types import GenerateContentConfig
from dotenv import load_dotenv
import json
import os
import requests

app = Flask(__name__)

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def find_country_from_ip(ip=None):
    url = "https://ipapi.co/json/" if ip is None else f"https://ipapi.co/{ip}/json/"
    data = requests.get(url, timeout=5).json()
    return data.get("country_name")

@app.route('/', methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        content = request.form["content"]
        country_name = find_country_from_ip()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=content,
            config=GenerateContentConfig(
                system_instruction=[
                    "You are a mental health therapist.",
                    "I will give you the message that the user has sent. Your job is to console the user and provide a listening ear to them.",
                    "You are not to respond to the user in a harsh tone or use inappropriate/vulgar language that can worsen their mood.",
                    f"Understand the user's problem and try to provide advice for them to solve their problem whenever appropriate. For context, the user is from {country_name}.",
                    "Please give your response in a HTML paragraph, you can omit the '```html' and '```' part of the code. There is no need to apply styling to the paragraph."
                ]
            )
        )
        output = response.text
        return render_template('index.html', output=output)
    return render_template('index.html')

app.run()
