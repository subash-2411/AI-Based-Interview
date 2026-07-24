import PyPDF2
import pdfplumber
import docx
import re
from dotenv import load_dotenv

load_dotenv()

# Load spaCy model (English) - Removed global load as it's unused and slows down runserver
nlp = None

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def extract_skills(text):
    # Predefined skill set (simplified for now)
    skill_db = [
        'Python', 'Django', 'Flask', 'FastAPI', 'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis',
        'Java', 'Spring', 'Spring Boot', 'Hibernate', 'C++', 'C', 'C#', '.NET', 'HTML', 'HTML5', 'CSS', 'CSS3', 'JavaScript', 'TypeScript',
        'React', 'React Native', 'Angular', 'Vue', 'Vue.js', 'Next.js', 'Nuxt.js', 'Node.js', 'Express.js',
        'Machine Learning', 'AI', 'NLP', 'Deep Learning', 'Computer Vision', 'Data Science', 'Pandas', 'NumPy',
        'Matplotlib', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'Keras',
        'AWS', 'Azure', 'GCP', 'Google Cloud', 'Firebase', 'Heroku',
        'Docker', 'Kubernetes', 'Terraform', 'CI/CD', 'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Jenkins', 'REST API', 'GraphQL', 'gRPC',
        'Agile', 'Scrum', 'Linux', 'Bash', 'PowerShell', 'Figma', 'UI/UX'
    ]
    
    extracted = []
    # Case insensitive search
    for skill in skill_db:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            extracted.append(skill)
    
    return extracted

def calculate_formatting_score(text):
    score = 100
    # Deduct for missing sections
    if not re.search(r'Experience|Work|Professional', text, re.I): score -= 15
    if not re.search(r'Education|University|College', text, re.I): score -= 15
    if not re.search(r'Project|Portfolio', text, re.I): score -= 15
    if not re.search(r'Skill|Technology|Tools', text, re.I): score -= 15
    # Deduct if no email or phone
    if not re.search(r'[\w\.-]+@[\w\.-]+', text): score -= 10
    if not re.search(r'(\d{10})', text): score -= 10
    # Deduct for bad length
    words = len(text.split())
    if words < 100: score -= 20
    elif words < 200: score -= 10
    return max(score, 30)

def calculate_impact_score(text):
    # Count action verbs
    action_verbs = ['led', 'developed', 'managed', 'designed', 'implemented', 'created', 
                    'delivered', 'optimized', 'built', 'improved', 'increased', 'reduced', 
                    'spearheaded', 'coordinated', 'achieved', 'established', 'launched']
    count = 0
    lower_text = text.lower()
    for verb in action_verbs:
        count += len(re.findall(r'\b' + verb + r'\b', lower_text))
    
    # Count metrics/numbers
    numbers = len(re.findall(r'\b\d+(?:%|\+)?\b', text))
    
    score = 45 + (count * 6) + (numbers * 8)
    return min(score, 100)

def calculate_clarity_score(text):
    # Simple readability heuristics
    words = text.split()
    if not words: return 0
    
    # Deduct for extremely long sentences
    sentences = re.split(r'[\.\!\?]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    long_sentences = sum(1 for s in sentences if len(s.split()) > 25)
    
    # Base score
    score = 90
    if len(sentences) > 0:
        pct_long = (long_sentences / len(sentences)) * 100
        score -= int(pct_long * 0.5)
        
    # Deduct for too short
    if len(words) < 150: score -= 15
    
    return max(score, 40)

def calculate_ats_score(text, analysis=None):
    # Dynamic ATS scoring
    score = 0
    
    # 1. Skill Density (Up to 40 points)
    found_skills = extract_skills(text)
    skill_score = min(len(found_skills) * 5, 40) # 8+ skills = max points
    score += skill_score
    
    # 2. Section Presence (Up to 30 points)
    sections_found = 0
    if re.search(r'Experience|Work|Professional', text, re.I): sections_found += 1
    if re.search(r'Education|University|College', text, re.I): sections_found += 1
    if re.search(r'Project|Portfolio', text, re.I): sections_found += 1
    if re.search(r'Skill|Technology|Tools', text, re.I): sections_found += 1
    
    score += (sections_found * 7.5)
    
    # 3. Contact Info (Up to 20 points)
    if re.search(r'[\w\.-]+@[\w\.-]+', text): score += 10 # Email
    if re.search(r'(\d{10})', text): score += 10 # Phone
    
    # 4. Length/Clarity (Up to 10 points)
    if len(text.split()) > 200: score += 10
    
    return min(score, 100)

def analyze_resume_with_ai(text):
    import os
    import json
    
    # 1. Contact Info fallback
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    phone = re.search(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{10})', text)
    
    # Try to find Name (Usually at the very top)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    name = lines[0] if lines else "Not Found"
    
    # Try to find Career Objective
    objective = "Not specified in resume"
    obj_match = re.search(r'(?:Objective|Career Objective|Professional Summary)(.*?)(?:\n\n|\r\n\r\n|Experience|Education|Skills)', text, re.S | re.I)
    if obj_match:
        objective = obj_match.group(1).strip()

    # Extract Experience years (simple heuristic)
    exp_years = 0
    exp_matches = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience', text, re.I)
    if exp_matches:
        exp_years = max([int(x) for x in exp_matches])

    is_fresher = exp_years == 0

    # Extract Education (Degrees)
    degrees = []
    degree_patterns = {
        'B.E. / B.Tech': r'\bB\.?E\.?\b|\bB\.?Tech\b|\bBachelor\s+of\s+Technology\b|\bBachelor\s+of\s+Engineering\b',
        'M.E. / M.Tech': r'\bM\.?E\.?\b|\bM\.?Tech\b|\bMaster\s+of\s+Technology\b|\bMaster\s+of\s+Engineering\b',
        'BCA': r'\bB\.?C\.?A\b|\bBachelor\s+of\s+Computer\s+Applications\b',
        'MCA': r'\bM\.?C\.?A\b|\bMaster\s+of\s+Computer\s+Applications\b',
        'B.Sc': r'\bB\.?S\.?c\b|\bBachelor\s+of\s+Science\b',
        'M.Sc': r'\bM\.?S\.?c\b|\bMaster\s+of\s+Science\b',
        'MBA': r'\bM\.?B\.?A\b|\bMaster\s+of\s+Business\s+Administration\b',
        'BBA': r'\bB\.?B\.?A\b|\bBachelor\s+of\s+Business\s+Administration\b',
        'B.Com': r'\bB\.?Com\b|\bBachelor\s+of\s+Commerce\b',
        'M.Com': r'\bM\.?Com\b|\bMaster\s+of\s+Commerce\b',
        'PhD': r'\bPhD\b|\bDoctor\s+of\s+Philosophy\b'
    }
    
    for degree_name, pattern in degree_patterns.items():
        if re.search(pattern, text, re.I):
            degrees.append(degree_name)

    # Compute deterministic scores
    formatting_score = calculate_formatting_score(text)
    impact_score = calculate_impact_score(text)
    clarity_score = calculate_clarity_score(text)
    ats_score = calculate_ats_score(text)

    fallback_analysis = {
        'name': name,
        'email': email.group(0) if email else "Not Found",
        'phone': phone.group(0) if phone else "Not Found",
        'objective': objective,
        'exp_years': exp_years,
        'is_fresher': is_fresher,
        'education': degrees if degrees else ["Not Specified"],
        'summary': "Profile demonstrates technical expertise.",
        'sections': {
            'Experience': len(re.findall(r'Experience|Work|Professional', text, re.I)) > 0,
            'Education': len(re.findall(r'Education|University|College', text, re.I)) > 0,
            'Projects': len(re.findall(r'Project|Portfolio', text, re.I)) > 0,
            'Certifications': len(re.findall(r'Certificate|Certified', text, re.I)) > 0,
        },
        'recommendations': [
            "Add more quantitative achievements.",
            "Ensure LinkedIn profile is linked.",
            "Include a summary section."
        ],
        'role_suggestions': ['Full Stack Developer', 'Software Engineer'],
        'missing_keywords': ['Docker', 'Kubernetes', 'CI/CD Pipelines', 'Cloud Services (AWS/GCP)'],
        'formatting_score': formatting_score,
        'impact_score': impact_score,
        'clarity_score': clarity_score,
        'ats_score': ats_score,
        'skills': extract_skills(text)
    }

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return fallback_analysis

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        You are an advanced Applicant Tracking System (ATS) and professional resume parser.
        Analyze the following resume text:
        
        {text[:4000]}
        
        Extract the following structured details. Return EXACTLY a JSON object with the following fields:
        - "name": The candidate's full name.
        - "email": The candidate's email address.
        - "phone": The candidate's phone number.
        - "objective": A concise summary of their professional background or objective.
        - "exp_years": Estimated years of professional experience (integer).
        - "is_fresher": A boolean indicating if they are a fresher (0 years of experience).
        - "education": A list of degrees detected (e.g. ["B.Tech", "MCA"]).
        - "summary": A brief one-sentence professional summary.
        - "sections": An object/dictionary with keys "Experience", "Education", "Projects", "Certifications" mapping to booleans indicating if each section is present in the resume.
        - "recommendations": A list of 3 specific, actionable recommendations to improve their resume for ATS compatibility. Do not use generic placeholders; write specific recommendations based on their content.
        - "role_suggestions": A list of 2-3 suitable job roles based on their skills.
        - "missing_keywords": A list of 3-4 industry-standard skills, frameworks, or methodologies that are currently missing from the resume but are highly recommended to add for real-world readiness in their targeted roles.
        - "skills": A list of technical skills detected (e.g., ["Python", "Django", "React"]).
        
        Ensure the JSON format is perfectly valid. Return ONLY the raw JSON text. Do not use ```json formatting.
        """
        response = model.generate_content(prompt, request_options={"timeout": 15.0})
        raw_text = response.text.strip()
        
        # Parse JSON
        match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if match:
            parsed = json.loads(match.group(0))
            # Merge with default fallback keys just in case some are missing
            for k, v in fallback_analysis.items():
                if k not in parsed:
                    parsed[k] = v
            
            # Enforce deterministic scores so they never fluctuate
            parsed['formatting_score'] = formatting_score
            parsed['impact_score'] = impact_score
            parsed['clarity_score'] = clarity_score
            parsed['ats_score'] = ats_score
            return parsed
    except Exception as e:
        print(f"Error in analyze_resume_with_ai: {e}")
        
    return fallback_analysis

