import PyPDF2
import pdfplumber
import docx
import re
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Predefined comprehensive industry skill set for heuristic extraction
SKILL_DB = [
    # Languages
    'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#', 'C', 'Go', 'Golang', 'Rust', 'PHP', 'Ruby', 'Swift', 'Kotlin', 'Dart', 'SQL', 'R', 'HTML', 'HTML5', 'CSS', 'CSS3', 'Sass', 'SCSS',
    # Frameworks & Libraries
    'Django', 'Flask', 'FastAPI', 'React', 'React.js', 'React Native', 'Angular', 'Vue', 'Vue.js', 'Next.js', 'Nuxt.js', 'Node.js', 'Express', 'Express.js', 'Spring', 'Spring Boot', 'Hibernate', '.NET', 'ASP.NET', 'Laravel', 'Flutter', 'Redux', 'Tailwind', 'TailwindCSS', 'Bootstrap', 'jQuery',
    # Data Science & AI
    'Machine Learning', 'Deep Learning', 'Artificial Intelligence', 'AI', 'NLP', 'Natural Language Processing', 'Computer Vision', 'Data Science', 'Pandas', 'NumPy', 'SciPy', 'Matplotlib', 'Seaborn', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'Keras', 'OpenCV', 'HuggingFace', 'LangChain', 'LLM', 'Gemini', 'OpenAI',
    # Databases & Caching
    'PostgreSQL', 'MySQL', 'SQLite', 'MongoDB', 'Redis', 'Cassandra', 'Elasticsearch', 'DynamoDB', 'Oracle', 'Firebase', 'Supabase',
    # Cloud & DevOps
    'AWS', 'Amazon Web Services', 'Azure', 'GCP', 'Google Cloud', 'Docker', 'Kubernetes', 'Terraform', 'CI/CD', 'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Jenkins', 'Linux', 'Unix', 'Bash', 'Shell', 'Nginx', 'Apache',
    # Methodologies & Architecture
    'REST API', 'RESTful', 'GraphQL', 'Microservices', 'System Design', 'Agile', 'Scrum', 'Jira', 'OOP', 'Object Oriented Programming', 'Data Structures', 'Algorithms', 'TDD', 'Unit Testing', 'Figma', 'UI/UX'
]

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception:
        # Fallback to PyPDF2
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            print(f"Error extracting PDF: {e}")
    return text

def extract_text_from_docx(docx_path):
    text = ""
    try:
        doc = docx.Document(docx_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += cell.text + " "
                text += "\n"
    except Exception as e:
        print(f"Error extracting DOCX: {e}")
    return text

def extract_skills(text):
    extracted = set()
    for skill in SKILL_DB:
        # Word boundary match with escape
        pattern = r'(?i)\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            extracted.add(skill)
    return sorted(list(extracted))

def calculate_formatting_score(text):
    """
    Evaluates resume formatting, structure, and presence of standard sections.
    Realistic score range: 50% - 95%.
    """
    score = 50 # Base score for parseable text
    
    # Check key section headers
    has_exp = bool(re.search(r'\b(Experience|Work Experience|Employment|Work History|Professional Experience)\b', text, re.I))
    has_edu = bool(re.search(r'\b(Education|Academic|Degree|University|College)\b', text, re.I))
    has_proj = bool(re.search(r'\b(Projects?|Portfolio|Key Projects|Academic Projects)\b', text, re.I))
    has_skills = bool(re.search(r'\b(Skills|Technical Skills|Core Competencies|Technologies|Tech Stack)\b', text, re.I))
    has_cert = bool(re.search(r'\b(Certifications?|Certificates?|Licences?|Awards)\b', text, re.I))
    has_summary = bool(re.search(r'\b(Summary|Professional Summary|Objective|Career Objective|About Me|Profile)\b', text, re.I))
    
    if has_exp: score += 10
    if has_edu: score += 8
    if has_proj: score += 8
    if has_skills: score += 8
    if has_cert: score += 5
    if has_summary: score += 5

    # Check contact info
    has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text))
    has_phone = bool(re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b', text))
    has_links = bool(re.search(r'linkedin\.com|github\.com|gitlab\.com|portfolio|\.dev|\.me', text, re.I))
    
    if has_email: score += 3
    if has_phone: score += 3
    if has_links: score += 4

    # Length optimization (ideal resume is between 300 and 800 words)
    words = len(text.split())
    if words < 120:
        score -= 15
    elif words < 250:
        score -= 8
    elif words > 1000:
        score -= 5

    return max(35, min(score, 95))

def calculate_impact_score(text):
    """
    Evaluates action verbs, quantifiable achievements, and metrics.
    Realistic score range: 45% - 90%.
    """
    action_verbs = [
        'architected', 'spearheaded', 'engineered', 'optimized', 'delivered', 'accelerated', 
        'overhauled', 'scaled', 'led', 'developed', 'implemented', 'streamlined', 'automated',
        'built', 'created', 'designed', 'launched', 'improved', 'increased', 'reduced',
        'boosted', 'generated', 'transformed', 'mentored', 'managed', 'deployed'
    ]
    
    lower_text = text.lower()
    verb_count = sum(len(re.findall(r'\b' + verb + r'\b', lower_text)) for verb in action_verbs)
    
    # Count quantifiable metrics (%, numbers, currency, multipliers)
    metrics = len(re.findall(r'\b(?:\d+%(?:\+)?|\d+\+|\$\d+[\d,]*|\d+(?:\.\d+)?(?:k|m|x|ms|s|%))\b', text, re.I))
    raw_numbers = len(re.findall(r'\b\d{2,}\b', text))
    total_metrics = metrics + (raw_numbers // 2)
    
    # Base calibrated score
    score = 40 + min(verb_count * 2.5, 25) + min(total_metrics * 4, 30)
    
    # Penalize vague passive phrases
    weak_phrases = ['responsible for', 'duties included', 'worked on', 'helped with', 'assisted in']
    weak_count = sum(len(re.findall(r'\b' + phrase + r'\b', lower_text)) for phrase in weak_phrases)
    score -= (weak_count * 3)
    
    return int(max(35, min(score, 92)))

def calculate_clarity_score(text):
    """
    Evaluates sentence structure, bullet point clarity, and readability.
    Realistic score range: 50% - 92%.
    """
    words = text.split()
    if not words:
        return 40
        
    sentences = [s.strip() for s in re.split(r'[\.\!\?\n]', text) if len(s.strip().split()) > 3]
    if not sentences:
        return 50
        
    # Long run-on sentences (>28 words) hurt ATS readability
    long_sentences = sum(1 for s in sentences if len(s.split()) > 28)
    long_ratio = long_sentences / len(sentences)
    
    score = 85
    score -= int(long_ratio * 40)
    
    # Check bullet points density
    has_bullets = bool(re.search(r'[•\-\*▪►]\s', text))
    if has_bullets:
        score += 8
    else:
        score -= 6
        
    if len(words) < 180:
        score -= 10
        
    return int(max(40, min(score, 94)))

def calculate_ats_score(text, analysis=None):
    """
    Weighted ATS composite score:
    - 30% Skill Match & Relevance
    - 25% Impact & Measurable Metrics
    - 20% Section Architecture & Formatting
    - 15% Contact & Online Footprint (LinkedIn, GitHub)
    - 10% Clarity & Readability
    """
    skills = extract_skills(text)
    formatting = calculate_formatting_score(text)
    impact = calculate_impact_score(text)
    clarity = calculate_clarity_score(text)
    
    # Skill component (0 - 30 pts): 4 skills = 12pts, 8 skills = 22pts, 12+ skills = 30pts
    skill_pts = min(len(skills) * 2.5, 30)
    
    # Impact component (0 - 25 pts)
    impact_pts = (impact / 100) * 25
    
    # Formatting component (0 - 20 pts)
    formatting_pts = (formatting / 100) * 20
    
    # Online Footprint & Contact (0 - 15 pts)
    footprint_pts = 5
    if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text): footprint_pts += 3
    if re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b', text): footprint_pts += 3
    if re.search(r'linkedin\.com|github\.com|gitlab\.com', text, re.I): footprint_pts += 4
    footprint_pts = min(footprint_pts, 15)
    
    # Clarity component (0 - 10 pts)
    clarity_pts = (clarity / 100) * 10
    
    composite = int(skill_pts + impact_pts + formatting_pts + footprint_pts + clarity_pts)
    return max(40, min(composite, 95))

def _safe_int(val, default=50):
    """Safely convert any value (e.g. '85%', '85/100', 85.5, None) to int."""
    if val is None:
        return default
    if isinstance(val, (int, float)):
        return int(val)
    try:
        # Extract the first integer match from string
        match = re.search(r'\d+', str(val))
        if match:
            return int(match.group(0))
        return int(float(val))
    except Exception:
        return default

def analyze_resume_with_ai(text):
    """
    Deep, accurate AI-powered ATS evaluation utilizing Google Gemini.
    Provides rigorous industry-standard scoring, section audits, and real-world recommendations.
    """
    # 1. Base deterministic extraction as fallback
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b', text)
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    detected_name = lines[0] if lines else "Candidate"
    
    objective = "Professional focused on delivering impactful software solutions."
    obj_match = re.search(r'(?:Objective|Career Objective|Professional Summary|About Me|Summary)(.*?)(?:\n\n|\r\n\r\n|Experience|Education|Skills|Projects)', text, re.S | re.I)
    if obj_match:
        clean_obj = obj_match.group(1).strip()
        if len(clean_obj) > 20:
            objective = clean_obj[:300]

    # Experience years
    exp_years = 0
    exp_matches = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience', text, re.I)
    if exp_matches:
        exp_years = max([int(x) for x in exp_matches])
    is_fresher = exp_years == 0

    # Degrees detected
    degrees = []
    degree_patterns = {
        'B.E. / B.Tech': r'\bB\.?E\.?\b|\bB\.?Tech\b|\bBachelor\s+of\s+Technology\b|\bBachelor\s+of\s+Engineering\b',
        'M.E. / M.Tech': r'\bM\.?E\.?\b|\bM\.?Tech\b|\bMaster\s+of\s+Technology\b|\bMaster\s+of\s+Engineering\b',
        'BCA': r'\bB\.?C\.?A\b|\bBachelor\s+of\s+Computer\s+Applications\b',
        'MCA': r'\bM\.?C\.?A\b|\bMaster\s+of\s+Computer\s+Applications\b',
        'B.Sc': r'\bB\.?S\.?c\b|\bBachelor\s+of\s+Science\b',
        'M.Sc': r'\bM\.?S\.?c\b|\bMaster\s+of\s+Science\b',
        'MBA': r'\bM\.?B\.?A\b|\bMaster\s+of\s+Business\s+Administration\b',
        'B.Com': r'\bB\.?Com\b|\bBachelor\s+of\s+Commerce\b',
        'PhD': r'\bPhD\b|\bDoctor\s+of\s+Philosophy\b'
    }
    for degree_name, pattern in degree_patterns.items():
        if re.search(pattern, text, re.I):
            degrees.append(degree_name)

    extracted_skills = extract_skills(text)
    formatting_score = calculate_formatting_score(text)
    impact_score = calculate_impact_score(text)
    clarity_score = calculate_clarity_score(text)
    ats_score = calculate_ats_score(text)

    # Contextual missing keywords suggestion
    default_missing = ['Docker', 'CI/CD Pipelines', 'Cloud Architecture (AWS/GCP)', 'Unit Testing']
    if 'Python' in extracted_skills:
        default_missing = ['FastAPI / Celery', 'Docker & Containerization', 'PostgreSQL Optimization', 'CI/CD Pipelines']
    elif 'React' in extracted_skills or 'JavaScript' in extracted_skills:
        default_missing = ['TypeScript', 'Next.js', 'State Management (Redux/Zustand)', 'Jest / Cypress Testing']

    fallback_analysis = {
        'name': detected_name,
        'email': email_match.group(0) if email_match else "Not Found",
        'phone': phone_match.group(0) if phone_match else "Not Found",
        'objective': objective,
        'exp_years': exp_years,
        'is_fresher': is_fresher,
        'education': degrees if degrees else ["Bachelor's Degree"],
        'summary': f"Technical profile with demonstrated skills in {', '.join(extracted_skills[:4]) if extracted_skills else 'software engineering'}.",
        'sections': {
            'Experience': bool(re.search(r'\b(Experience|Work|Employment)\b', text, re.I)),
            'Education': bool(re.search(r'\b(Education|College|University)\b', text, re.I)),
            'Projects': bool(re.search(r'\b(Projects?|Portfolio)\b', text, re.I)),
            'Certifications': bool(re.search(r'\b(Certificat|Certified|Licence)\b', text, re.I)),
            'Skills': bool(re.search(r'\b(Skills|Technologies|Tech Stack)\b', text, re.I))
        },
        'recommendations': [
            "Quantify bullet points with measurable impact (e.g., % improvement, scale of users, latency reduction).",
            "Include direct links to your active GitHub repositories or live project demos.",
            "Add a dedicated Skills matrix categorizing Languages, Frameworks, and Cloud tools."
        ],
        'role_suggestions': ['Full Stack Developer', 'Software Engineer', 'Backend Developer'],
        'missing_keywords': default_missing,
        'formatting_score': formatting_score,
        'impact_score': impact_score,
        'clarity_score': clarity_score,
        'ats_score': ats_score,
        'skills': extracted_skills
    }

    raw_api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""
    valid_keys = [k.strip() for k in raw_api_key.split(',') if k.strip()]
    if not valid_keys:
        return fallback_analysis

    # Try calling Gemini with primary and fallback models
    models_to_try = ['gemini-2.5-flash', 'gemini-2.5-pro']
    
    try:
        import google.generativeai as genai
        clean_api_key = valid_keys[0]
        genai.configure(api_key=clean_api_key)
        
        prompt = f"""
You are an expert ATS (Applicant Tracking System) Auditor, Technical Hiring Manager, and Senior Recruiter.
Analyze the following resume with high rigor, objectivity, and precision (comparable to Jobscan, Taleo, and Workday ATS algorithms).

--- RESUME TEXT ---
{text[:4500]}
--- END RESUME TEXT ---

EVALUATION CRITERIA:
1. ATS SCORE (0-100):
   - 88 - 98: Top 5% exceptional resume. Strong quantified business achievements (e.g., "+35% speed", "handled 100k requests/sec"), comprehensive modern tech stack, clean standard headings, GitHub/LinkedIn links.
   - 74 - 87: Solid resume with good technical skills, but has slight keyword gaps or lacks sufficient quantified metrics.
   - 58 - 73: Average resume. Mostly lists job responsibilities rather than achievements; lacks metrics or modern tools.
   - Below 58: Incomplete sections, sparse skills, poor formatting, or vague statements.
   DO NOT give an arbitrary 100 or 95 unless the resume is truly flawless with heavy numbers, metrics, and complete sections.

2. SUB-METRICS:
   - "formatting_score": (0-100) Structural readability, standard headers, contact info presence.
   - "impact_score": (0-100) Density of measurable results, numbers, percentages, and strong action verbs.
   - "clarity_score": (0-100) Conciseness, bullet point quality, absence of fluff/long paragraphs.

Return ONLY a valid JSON object with EXACTLY these keys:
{{
    "name": "Candidate Full Name",
    "email": "Email Address or 'Not Found'",
    "phone": "Phone Number or 'Not Found'",
    "objective": "A 1-2 sentence professional summary or objective extracted from the resume",
    "exp_years": 0,
    "is_fresher": true,
    "education": ["B.Tech Computer Science", "etc."],
    "summary": "1-sentence executive recruiter summary of this candidate's profile",
    "sections": {{
        "Experience": true,
        "Education": true,
        "Projects": true,
        "Certifications": false,
        "Skills": true
    }},
    "skills": ["Skill1", "Skill2", "Skill3", "...all technical and domain skills detected..."],
    "ats_score": 72,
    "formatting_score": 80,
    "impact_score": 65,
    "clarity_score": 78,
    "recommendations": [
        "Actionable recommendation 1 tailored specifically to this candidate",
        "Actionable recommendation 2 tailored specifically to this candidate",
        "Actionable recommendation 3 tailored specifically to this candidate"
    ],
    "role_suggestions": ["Role 1", "Role 2", "Role 3"],
    "missing_keywords": ["Crucial Missing Skill 1", "Crucial Missing Tool 2", "Crucial Missing Tech 3", "Crucial Missing Tool 4"]
}}

CRITICAL: Return ONLY the JSON object. Do not include markdown blocks or any conversational text.
"""
        
        response = None
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt, request_options={"timeout": 9.0})
                if response and response.text:
                    break
            except Exception as model_err:
                print(f"Model {model_name} failed: {model_err}, trying fallback...")
                continue

        if response and response.text:
            raw_text = response.text.strip()
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))
                
                # Ensure all required fields exist
                for k, v in fallback_analysis.items():
                    if k not in parsed:
                        parsed[k] = v
                
                # Clamp scores between realistic ranges (30 to 98) safely
                parsed['ats_score'] = max(30, min(_safe_int(parsed.get('ats_score'), ats_score), 98))
                parsed['formatting_score'] = max(30, min(_safe_int(parsed.get('formatting_score'), formatting_score), 98))
                parsed['impact_score'] = max(30, min(_safe_int(parsed.get('impact_score'), impact_score), 98))
                parsed['clarity_score'] = max(30, min(_safe_int(parsed.get('clarity_score'), clarity_score), 98))
                
                if not parsed.get('skills') or not isinstance(parsed.get('skills'), list):
                    parsed['skills'] = extracted_skills
                
                return parsed
    except Exception as e:
        print(f"Error in analyze_resume_with_ai (using fallback): {e}")

    return fallback_analysis
