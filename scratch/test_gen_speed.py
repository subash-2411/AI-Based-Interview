import os
import time
from dotenv import load_dotenv
load_dotenv()

from ai_engine.logic import generate_questions

print("Starting question generation...")
start_time = time.time()
skills = ["Python", "Django", "React"]
qs = generate_questions(skills, count=5, language='en-US', difficulty='Intermediate')
end_time = time.time()

print(f"Questions: {qs}")
print(f"Time taken: {end_time - start_time:.2f} seconds")
