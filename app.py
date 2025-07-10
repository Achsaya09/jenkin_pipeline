from flask import Flask, render_template, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Groq client
client = Groq(api_key="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")

def generate_with_groq(prompt, max_tokens=300, temperature=0.8):
    """Helper function to generate content with Groq"""
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating content: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_story', methods=['POST'])
def generate_story():
    try:
        data = request.get_json()
        word = data.get('word', '').strip()
        
        if not word:
            return jsonify({'error': 'Please provide a word'}), 400
        
        prompt = f"Write a creative short story (100-150 words) based on this word: {word}"
        story = generate_with_groq(prompt)
        return jsonify({'result': story})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_poem', methods=['POST'])
def generate_poem():
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        style = data.get('style', 'romantic')
        
        if not topic:
            return jsonify({'error': 'Please provide a topic'}), 400
            
        prompt = f"Write a {style} poem about {topic}. Make it creative and engaging, 8-12 lines long."
        poem = generate_with_groq(prompt, temperature=0.9)
        return jsonify({'result': poem})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate_joke', methods=['POST'])
def generate_joke():
    try:
        data = request.get_json()
        topic = data.get('topic', 'general')
        
        prompt = f"Tell me a funny, clean joke about {topic}. Keep it short and witty, just one or two sentences."
        joke = generate_with_groq(prompt, temperature=1.0, max_tokens=150)
        return jsonify({'result': joke})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
