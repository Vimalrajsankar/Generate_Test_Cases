
from flask import Flask, render_template, request
import textwrap
import os
import google.generativeai as genai

app = Flask(__name__)


os.environ['GOOGLE_API_KEY'] = "****************************" 


genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')


import textwrap
import re

def to_markdown(text):
    text = text.replace('•', '  *')   
    return textwrap.indent(re.sub(r'\*\*', '', text), ' ', predicate=lambda _: True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    queries = request.form.getlist('query')

    generated_content = []
    for query in queries:
        response = model.generate_content(query)
        formatted_response = to_markdown(response.text)
        generated_content.append(formatted_response)

    return render_template('index.html', queries=queries, generated_content=generated_content)

if __name__ == '__main__':
    app.run(debug=True)
 