import os
import time
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai

genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

models_to_test = [
    'gemini-flash-latest',
    'gemini-2.0-flash',
    'gemini-2.5-flash',
    'gemini-3.5-flash'
]

skills = ["Python", "Django", "React"]
prompt = f"Generate exactly 5 unique, non-repeating interview questions based on skills: {', '.join(skills)}. Keep them concise. Format as a list of questions, one per line. Do not include numbers."

for model_name in models_to_test:
    try:
        model = genai.GenerativeModel(model_name)
        start = time.time()
        response = model.generate_content(prompt)
        duration = time.time() - start
        print(f"Model: {model_name} | Time: {duration:.2f}s | Response lines: {len(response.text.strip().splitlines())}")
    except Exception as e:
        print(f"Model: {model_name} failed: {e}")
