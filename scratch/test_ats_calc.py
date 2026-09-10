import os
import sys
import django

# Add project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from resume.utils import analyze_resume_with_ai, calculate_ats_score, calculate_formatting_score, calculate_impact_score, calculate_clarity_score

sample_fresher_resume = """
John Doe
johndoe@gmail.com | 9876543210 | Chennai, India
linkedin.com/in/johndoe | github.com/johndoe

CAREER OBJECTIVE
Enthusiastic Computer Science graduate seeking an entry-level software engineer role to apply problem-solving skills and develop scalable applications.

EDUCATION
B.Tech in Computer Science and Engineering - Anna University (2020 - 2024) | CGPA: 8.4/10

TECHNICAL SKILLS
Languages: Python, JavaScript, C++, HTML, CSS, SQL
Frameworks: Django, React, Bootstrap
Databases: MySQL, PostgreSQL
Tools: Git, GitHub, VS Code

PROJECTS
1. E-Commerce Web Application (Django, React, PostgreSQL)
- Developed full-stack online store with user authentication, product catalog, and cart system.
- Integrated Stripe payment gateway and order tracking features.
- Hosted on Heroku with 99.9% uptime.

2. Student Management System (Python, MySQL)
- Built desktop database management tool for college administration handling 1,500+ student records.
- Automated grade calculation and report generation reducing manual effort by 40%.

CERTIFICATIONS
- Python for Data Science - Coursera (2023)
- Full Stack Web Development Bootcamp (2024)
"""

print("=== Testing Fallback Heuristic Scores ===")
f_score = calculate_formatting_score(sample_fresher_resume)
i_score = calculate_impact_score(sample_fresher_resume)
c_score = calculate_clarity_score(sample_fresher_resume)
ats_raw = calculate_ats_score(sample_fresher_resume)
print(f"Formatting: {f_score}%, Impact: {i_score}%, Clarity: {c_score}%, ATS Score: {ats_raw}%")

print("\n=== Testing Deep AI ATS Evaluation ===")
ai_result = analyze_resume_with_ai(sample_fresher_resume)
print(f"Candidate: {ai_result.get('name')}")
print(f"ATS Score: {ai_result.get('ats_score')}%")
print(f"Formatting Score: {ai_result.get('formatting_score')}%")
print(f"Impact Score: {ai_result.get('impact_score')}%")
print(f"Clarity Score: {ai_result.get('clarity_score')}%")
print(f"Extracted Skills ({len(ai_result.get('skills', []))}): {ai_result.get('skills')}")
print(f"Missing Keywords: {ai_result.get('missing_keywords')}")
print(f"Recommendations: {ai_result.get('recommendations')}")
