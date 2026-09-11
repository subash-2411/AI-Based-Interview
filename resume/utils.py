import PyPDF2
import pdfplumber
import docx
import re
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Predefined comprehensive industry skill set for heuristic extraction
# Predefined comprehensive industry skill set for heuristic extraction (IT & Non-IT)
SKILL_DB = [
    # Languages
    'Python', 'JavaScript', 'TypeScript', 'Java', 'C++', 'C#', 'C', 'Go', 'Golang', 'Rust', 'PHP', 'Ruby', 'Swift', 'Kotlin', 'Dart', 'SQL', 'R', 'HTML', 'HTML5', 'CSS', 'CSS3', 'Sass', 'SCSS',
    # Frameworks & Libraries
    'Django', 'Flask', 'FastAPI', 'React', 'React.js', 'React Native', 'Angular', 'Vue', 'Vue.js', 'Next.js', 'Nuxt.js', 'Node.js', 'Express', 'Express.js', 'Spring', 'Spring Boot', 'Hibernate', '.NET', 'ASP.NET', 'Laravel', 'Flutter', 'Redux', 'Tailwind', 'TailwindCSS', 'Bootstrap', 'jQuery',
    # Data Science & AI
    'Machine Learning', 'Deep Learning', 'Artificial Intelligence', 'AI', 'NLP', 'Natural Language Processing', 'Computer Vision', 'Data Science', 'Pandas', 'NumPy', 'SciPy', 'Matplotlib', 'Seaborn', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'Keras', 'OpenCV', 'HuggingFace', 'LangChain', 'LLM', 'Gemini', 'OpenAI', 'PowerBI', 'Tableau',
    # Databases & Caching
    'PostgreSQL', 'MySQL', 'SQLite', 'MongoDB', 'Redis', 'Cassandra', 'Elasticsearch', 'DynamoDB', 'Oracle', 'Firebase', 'Supabase',
    # Cloud & DevOps
    'AWS', 'Amazon Web Services', 'Azure', 'GCP', 'Google Cloud', 'Docker', 'Kubernetes', 'Terraform', 'CI/CD', 'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Jenkins', 'Linux', 'Unix', 'Bash', 'Shell', 'Nginx', 'Apache',
    # Methodologies & Architecture
    'REST API', 'RESTful', 'GraphQL', 'Microservices', 'System Design', 'Agile', 'Scrum', 'Jira', 'OOP', 'Object Oriented Programming', 'Data Structures', 'Algorithms', 'TDD', 'Unit Testing', 'Figma', 'UI/UX',
    # Commerce, Accounting & Finance (Non-IT)
    'Tally', 'Tally Prime', 'Tally ERP', 'GST', 'GST Filing', 'Income Tax', 'Taxation', 'TDS', 'Financial Accounting', 'Cost Accounting', 'Management Accounting', 'Auditing', 'Bookkeeping', 'Balance Sheet', 'Trial Balance', 'Ledger', 'Bank Reconciliation', 'BRS', 'Payroll Management', 'Accounts Payable', 'Accounts Receivable', 'Financial Modeling', 'Budgeting', 'Forecasting', 'Excel', 'Advanced Excel', 'VLOOKUP', 'Pivot Tables', 'MIS Reporting', 'SAP FICO', 'QuickBooks', 'Zoho Books',
    # Management, HR, Sales & Marketing (Non-IT)
    'Business Development', 'Sales', 'Lead Generation', 'Client Relations', 'CRM', 'Digital Marketing', 'SEO', 'Content Marketing', 'Human Resources', 'HR Operations', 'Talent Acquisition', 'Recruitment', 'Employee Relations', 'Performance Management', 'Vendor Management', 'Operations Management'
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
    text_chunks = []
    try:
        doc = docx.Document(docx_path)
        
        # 1. Header and footer text (where candidate contact info, LinkedIn, GitHub often live)
        for section in doc.sections:
            try:
                if section.header:
                    for hp in section.header.paragraphs:
                        if hp.text.strip(): text_chunks.append(hp.text.strip())
                if section.footer:
                    for fp in section.footer.paragraphs:
                        if fp.text.strip(): text_chunks.append(fp.text.strip())
            except Exception:
                pass

        # 2. Main body paragraphs
        for para in doc.paragraphs:
            if para.text.strip():
                text_chunks.append(para.text.strip())
                
        # 3. Tables
        for table in doc.tables:
            for row in table.rows:
                row_texts = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_texts:
                    text_chunks.append(" | ".join(row_texts))
                    
        # 4. Hyperlink relationships (e.g. LinkedIn, GitHub, portfolio links)
        try:
            for rel in doc.part.rels.values():
                if hasattr(rel, 'reltype') and "hyperlink" in str(rel.reltype).lower():
                    target = str(getattr(rel, 'target_ref', ''))
                    if target and any(k in target.lower() for k in ['linkedin', 'github', 'http', 'mailto', 'gitlab', 'portfolio']):
                        text_chunks.append(target)
        except Exception:
            pass

    except Exception as e:
        print(f"Error extracting DOCX: {e}")
        
    return "\n".join(text_chunks)

def extract_skills(text):
    extracted = set()
    for skill in SKILL_DB:
        pattern = r'(?i)\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            extracted.add(skill)
    return sorted(list(extracted))

def calculate_formatting_score(text):
    words = len(text.split())
    if words < 15:
        return 15
        
    score = 45
    has_exp = bool(re.search(r'\b(Experience|Work Experience|Employment|Work History|Professional Experience)\b', text, re.I))
    has_edu = bool(re.search(r'\b(Education|Academic|Degree|University|College|School|HSC|SSLC)\b', text, re.I))
    has_proj = bool(re.search(r'\b(Projects?|Portfolio|Key Projects|Academic Projects)\b', text, re.I))
    has_skills = bool(re.search(r'\b(Skills|Technical Skills|Core Competencies|Technologies|Tech Stack|Expertise)\b', text, re.I))
    has_cert = bool(re.search(r'\b(Certifications?|Certificates?|Licences?|Awards)\b', text, re.I))
    has_summary = bool(re.search(r'\b(Summary|Professional Summary|Objective|Career Objective|About Me|Profile)\b', text, re.I))
    
    if has_exp: score += 10
    if has_edu: score += 8
    if has_proj: score += 8
    if has_skills: score += 8
    if has_cert: score += 5
    if has_summary: score += 5

    has_email = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text))
    has_phone = bool(re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b', text))
    has_links = bool(re.search(r'linkedin\.com|github\.com|gitlab\.com|portfolio|\.dev|\.me', text, re.I))
    
    if has_email: score += 4
    if has_phone: score += 4
    if has_links: score += 4

    if words < 50:
        score -= 25
    elif words < 120:
        score -= 12
    elif words > 1200:
        score -= 5

    return max(10, min(score, 95))

def calculate_impact_score(text):
    words = len(text.split())
    if words < 15:
        return 10
        
    action_verbs = [
        'architected', 'spearheaded', 'engineered', 'optimized', 'delivered', 'accelerated', 
        'overhauled', 'scaled', 'led', 'developed', 'implemented', 'streamlined', 'automated',
        'built', 'created', 'designed', 'launched', 'improved', 'increased', 'reduced',
        'boosted', 'generated', 'transformed', 'mentored', 'managed', 'deployed', 'maintained',
        'prepared', 'analyzed', 'reconciled', 'coordinated', 'audited', 'negotiated'
    ]
    
    lower_text = text.lower()
    verb_count = sum(len(re.findall(r'\b' + verb + r'\b', lower_text)) for verb in action_verbs)
    metrics = len(re.findall(r'\b(?:\d+%(?:\+)?|\d+\+|\$\d+[\d,]*|\d+(?:\.\d+)?(?:k|m|x|ms|s|%|lakhs?|cr))\b', text, re.I))
    raw_numbers = len(re.findall(r'\b\d{2,}\b', text))
    total_metrics = metrics + (raw_numbers // 2)
    
    score = 35 + min(verb_count * 3, 25) + min(total_metrics * 4, 30)
    return int(max(10, min(score, 92)))

def calculate_clarity_score(text):
    words = text.split()
    if len(words) < 15:
        return 10
        
    sentences = [s.strip() for s in re.split(r'[\.\!\?\n]', text) if len(s.strip().split()) > 3]
    if not sentences:
        return 35
        
    long_sentences = sum(1 for s in sentences if len(s.split()) > 28)
    long_ratio = long_sentences / len(sentences)
    
    score = 85 - int(long_ratio * 40)
    has_bullets = bool(re.search(r'[•\-\*▪►]\s', text))
    if has_bullets: score += 6
    else: score -= 5
        
    return int(max(15, min(score, 94)))

def calculate_ats_score(text, analysis=None):
    words = len(text.split())
    if words < 15:
        return 15.0
        
    skills = extract_skills(text)
    formatting = calculate_formatting_score(text)
    impact = calculate_impact_score(text)
    clarity = calculate_clarity_score(text)
    
    skill_pts = min(len(skills) * 3.0, 30)
    impact_pts = (impact / 100) * 25
    formatting_pts = (formatting / 100) * 20
    
    footprint_pts = 3
    if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text): footprint_pts += 4
    if re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b', text): footprint_pts += 4
    if re.search(r'linkedin\.com|github\.com|gitlab\.com', text, re.I): footprint_pts += 4
    footprint_pts = min(footprint_pts, 15)
    
    clarity_pts = (clarity / 100) * 10
    composite = skill_pts + impact_pts + formatting_pts + footprint_pts + clarity_pts
    # Round to nearest integer — normalizes minor text extraction differences
    # so same resume as PDF or DOCX always shows the same ATS score
    composite = round(composite)
    return float(max(15, min(composite, 98)))

def _safe_int(val, default=0):
    try:
        if val is None: return default
        match = re.search(r'\d+', str(val))
        return int(match.group(0)) if match else int(float(val))
    except Exception:
        return default

def _safe_float(val, default=0.0):
    try:
        if val is None: return default
        match = re.search(r'\d+(\.\d+)?', str(val))
        return float(match.group(0)) if match else float(val)
    except Exception:
        return default

def get_smart_role_suggestions(skills, degrees, is_commerce, is_tech, is_dummy):
    """
    Dynamically generates 5–7 precise job roles based on the candidate's actual skills.
    STRICT RULE: React.js Developer is ONLY suggested if 'react' or 'react.js' is
    explicitly present in the extracted skill set.
    """
    if is_dummy:
        return ["Entry Level Trainee", "Data Entry Operator", "Junior Support Executive", "Operations Intern"]

    skill_set = {s.lower() for s in skills}
    roles = []

    # ── SCORE each domain by how many matching skills the candidate has ──
    has_react      = any(s in skill_set for s in ['react', 'react.js', 'react native'])
    has_frontend   = any(s in skill_set for s in ['vue', 'vue.js', 'angular', 'next.js', 'tailwind', 'tailwindcss', 'bootstrap', 'jquery', 'figma', 'sass', 'scss'])
    has_html_css_js= any(s in skill_set for s in ['html', 'html5', 'css', 'css3', 'javascript', 'typescript'])
    has_python     = any(s in skill_set for s in ['python'])
    has_django     = any(s in skill_set for s in ['django', 'flask', 'fastapi'])
    has_ai         = any(s in skill_set for s in ['machine learning', 'deep learning', 'artificial intelligence', 'ai', 'nlp',
                                                   'natural language processing', 'computer vision', 'data science',
                                                   'scikit-learn', 'tensorflow', 'pytorch', 'keras', 'huggingface',
                                                   'langchain', 'llm', 'gemini', 'openai', 'pandas', 'numpy'])
    has_data       = any(s in skill_set for s in ['powerbi', 'tableau', 'data science', 'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn'])
    has_backend    = any(s in skill_set for s in ['java', 'spring', 'spring boot', 'node.js', 'express', 'express.js',
                                                   'c++', 'c#', 'golang', 'go', 'rust', 'php', 'ruby', 'kotlin', '.net', 'asp.net'])
    has_db         = any(s in skill_set for s in ['sql', 'mysql', 'postgresql', 'sqlite', 'mongodb', 'redis',
                                                   'cassandra', 'oracle', 'firebase', 'dynamodb'])
    has_devops     = any(s in skill_set for s in ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'google cloud',
                                                   'terraform', 'ci/cd', 'linux', 'jenkins', 'git', 'github'])

    # ── 1. AI / ML / Data Science (highest priority if present) ──
    if has_ai:
        if has_python:
            roles.extend(["AI/ML Engineer", "Python AI Developer", "Machine Learning Specialist"])
        else:
            roles.extend(["Machine Learning Engineer", "AI Solutions Architect", "Data Science Analyst"])
        if has_data:
            roles.append("Data Science & Analytics Lead")

    # ── 2. Python / Django / Flask / FastAPI Backend ──
    if has_python or has_django:
        if has_django:
            roles.extend(["Django Backend Developer", "Python Full Stack Developer"])
        else:
            roles.extend(["Python Backend Developer", "Python Software Engineer"])
        if has_db:
            roles.append("Python API & Database Engineer")

    # ── 3. Database / SQL ──
    if has_db and not has_python and not has_ai:
        roles.extend(["SQL Database Developer", "Database Administrator", "Data Engineer"])

    # ── 4. React (ONLY if react/react.js explicitly detected) ──
    if has_react:
        roles.extend(["React.js Developer", "Frontend React Engineer", "React & Node Full Stack Developer"])

    # ── 5. Other Frontend Frameworks (Vue, Angular, Next.js etc.) — NOT React ──
    if has_frontend and not has_react:
        roles.extend(["Frontend Engineer", "UI/UX Web Developer", "JavaScript Framework Developer"])

    # ── 6. HTML/CSS/JS only (vanilla, no React/framework) ──
    if has_html_css_js and not has_react and not has_frontend:
        roles.extend(["Web Developer", "UI Developer", "Frontend Web Engineer"])

    # ── 7. General Backend (Java, Node, Go, C++ etc.) ──
    if has_backend:
        roles.extend(["Backend Software Engineer", "Systems & Application Developer"])
        if has_devops:
            roles.append("DevOps & Backend Engineer")

    # ── 8. DevOps / Cloud (only if explicitly dominant) ──
    if has_devops and not has_backend and not has_python:
        roles.extend(["DevOps Engineer", "Cloud Infrastructure Engineer", "Site Reliability Engineer"])

    # ── 9. Commerce, Accounting & Finance (Non-IT) ──
    if is_commerce or any(s in skill_set for s in ['tally', 'tally prime', 'tally erp', 'gst', 'gst filing',
                                                    'taxation', 'tds', 'auditing', 'bookkeeping', 'ledger',
                                                    'financial accounting', 'cost accounting']):
        roles.extend(["Financial Accountant", "Senior Accounts Executive",
                      "Tax & GST Consultant", "Auditing & Banking Analyst", "Corporate Finance Associate"])

    # ── 10. HR / Sales / Management ──
    if any(s in skill_set for s in ['human resources', 'hr operations', 'recruitment', 'talent acquisition',
                                     'sales', 'business development', 'operations management', 'crm']):
        roles.extend(["HR Operations Specialist", "Talent Acquisition Lead",
                      "Business Development Executive", "Operations Manager"])

    # ── Deduplicate while preserving order ──
    seen = set()
    distinct_roles = []
    for r in roles:
        if r not in seen:
            seen.add(r)
            distinct_roles.append(r)

    # ── Fill to minimum 5 roles if too few ──
    if len(distinct_roles) < 5:
        if is_commerce:
            for r in ["Accountant", "Finance Associate", "Accounts Manager", "Taxation Executive", "Audit Officer"]:
                if r not in seen:
                    distinct_roles.append(r)
                    seen.add(r)
        elif is_tech:
            for r in ["Software Engineer", "Technical Analyst", "Application Developer", "Systems Analyst", "IT Consultant"]:
                if r not in seen:
                    distinct_roles.append(r)
                    seen.add(r)
        else:
            for r in ["Associate Professional", "Operations Executive", "Business Analyst", "Project Coordinator", "Customer Success Lead"]:
                if r not in seen:
                    distinct_roles.append(r)
                    seen.add(r)

    # Return top 6 roles
    return distinct_roles[:6]

def analyze_resume_with_ai(text):
    """
    Ultra-fast, accurate AI-powered ATS evaluation.
    Accurately scores PDF and DOCX identically and delivers diverse, role-tailored career suggestions.
    """
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b', text)
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    detected_name = lines[0] if lines else "Candidate"
    
    words_count = len(text.split())
    is_dummy_resume = words_count < 25

    # Degrees detected
    degrees = []
    degree_patterns = {
        'B.Com': r'\bB\.?Com\b|\bBachelor\s+of\s+Commerce\b',
        'M.Com': r'\bM\.?Com\b|\bMaster\s+of\s+Commerce\b',
        'BBA': r'\bB\.?B\.?A\b|\bBachelor\s+of\s+Business\s+Administration\b',
        'MBA': r'\bM\.?B\.?A\b|\bMaster\s+of\s+Business\s+Administration\b',
        'CA / CMA': r'\bChartered\s+Accountant\b|\bCA\s+Inter\b|\bCMA\b|\bICWA\b',
        'B.E. / B.Tech': r'\bB\.?E\.?\b|\bB\.?Tech\b|\bBachelor\s+of\s+Technology\b|\bBachelor\s+of\s+Engineering\b',
        'M.E. / M.Tech': r'\bM\.?E\.?\b|\bM\.?Tech\b|\bMaster\s+of\s+Technology\b',
        'BCA': r'\bB\.?C\.?A\b|\bBachelor\s+of\s+Computer\s+Applications\b',
        'MCA': r'\bM\.?C\.?A\b|\bMaster\s+of\s+Computer\s+Applications\b',
        'B.Sc': r'\bB\.?S\.?c\b|\bBachelor\s+of\s+Science\b',
        'M.Sc': r'\bM\.?S\.?c\b|\bMaster\s+of\s+Science\b',
        'Diploma / ITI': r'\bDiploma\b|\bITI\b|\bPolytechnic\b',
        'PhD': r'\bPhD\b|\bDoctor\s+of\s+Philosophy\b'
    }
    for degree_name, pattern in degree_patterns.items():
        if re.search(pattern, text, re.I):
            degrees.append(degree_name)

    extracted_skills = extract_skills(text)
    
    is_commerce = any(d in ['B.Com', 'M.Com', 'BBA', 'MBA', 'CA / CMA'] for d in degrees) or bool(re.search(r'\b(commerce|accounting|accounts|tally|gst|taxation|auditing|finance|ledger|balance sheet|invoicing)\b', text, re.I))
    is_tech = bool(set(extracted_skills) & {'Python', 'Java', 'C++', 'JavaScript', 'Django', 'React', 'HTML', 'CSS', 'SQL', 'Node.js', 'Flutter'})
    
    smart_roles = get_smart_role_suggestions(extracted_skills, degrees, is_commerce, is_tech, is_dummy_resume)

    if is_dummy_resume:
        missing_keywords = ["Key Work Experience", "Educational Qualifications", "Domain Skillset", "Contact Details"]
        summary = "Resume contains minimal text. Add complete work history, education, and skills for full evaluation."
    elif is_commerce and not is_tech:
        missing_keywords = ["Tally Prime / ERP", "GST & TDS Filing", "Advanced Excel (Pivot, VLOOKUP)", "Bank Reconciliation (BRS)", "Balance Sheet Preparation"]
        summary = f"Commerce & Finance candidate with key proficiencies in {', '.join(extracted_skills[:3]) if extracted_skills else 'Accounting and Financial Reporting'}."
    else:
        missing_keywords = ["Docker & Containers", "CI/CD Deployment", "Cloud Platforms (AWS/GCP)", "Automated Unit Testing"]
        summary = f"Candidate specializing in {', '.join(extracted_skills[:4]) if extracted_skills else 'core domain competencies'}."

    formatting_score = calculate_formatting_score(text)
    impact_score = calculate_impact_score(text)
    clarity_score = calculate_clarity_score(text)
    ats_score = calculate_ats_score(text)

    fallback_analysis = {
        'name': detected_name,
        'email': email_match.group(0) if email_match else "Not Found",
        'phone': phone_match.group(0) if phone_match else "Not Found",
        'objective': "Dedicated professional aiming to leverage expertise and drive organizational success.",
        'exp_years': 0,
        'is_fresher': True,
        'education': degrees if degrees else (["Bachelor of Commerce (B.Com)"] if is_commerce else ["Bachelor's Degree"]),
        'summary': summary,
        'sections': {
            'Experience': bool(re.search(r'\b(Experience|Work|Employment)\b', text, re.I)),
            'Education': bool(re.search(r'\b(Education|College|University)\b', text, re.I)),
            'Projects': bool(re.search(r'\b(Projects?|Portfolio)\b', text, re.I)),
            'Certifications': bool(re.search(r'\b(Certificat|Certified|Licence)\b', text, re.I)),
            'Skills': bool(re.search(r'\b(Skills|Technologies|Tech Stack|Competencies)\b', text, re.I))
        },
        'strengths': [
            "Clean layout structure that ATS parsers interpret without distortion.",
            "Strong relevant keyword matching for the candidate's core domain.",
            "Standard headings that automated recruitment scanners readily index."
        ],
        'areas_for_improvement': [
            "1. Quantifiable Metrics: Include measurable numbers (e.g., % efficiency, revenue managed, scale of users).",
            "2. Tool Certifications: Mention relevant software licenses and certifications to boost ATS relevance.",
            "3. Action Verbs: Begin bullet points with strong active verbs like Architected, Reconciled, Developed, Spearheaded."
        ],
        'role_suggestions': smart_roles,
        'missing_keywords': missing_keywords,
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

    try:
        import google.generativeai as genai
        genai.configure(api_key=valid_keys[0])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
You are a top-tier ATS Auditor and Senior Recruiter.
Analyze this resume concisely and objectively.

--- RESUME TEXT ---
{text[:4000]}
--- END RESUME TEXT ---

CRITICAL RULES FOR role_suggestions:
- ONLY suggest "React.js Developer" if the word "React" or "React.js" explicitly appears in the resume text.
- If the candidate's top skills are Python, Django, Flask, AI, or SQL — suggest Python/Django/AI/Backend roles ONLY.
- role_suggestions MUST contain 5 to 7 specific, non-generic job roles that strictly match this candidate's exact tools and background.
- DO NOT suggest frontend or React roles based solely on HTML/CSS/JavaScript presence.

Return ONLY a JSON object:
{{
    "name": "{detected_name}",
    "email": "{email_match.group(0) if email_match else 'Not Found'}",
    "phone": "{phone_match.group(0) if phone_match else 'Not Found'}",
    "objective": "Concise professional objective",
    "exp_years": 0,
    "is_fresher": true,
    "education": ["Degree"],
    "summary": "1-sentence executive recruiter summary",
    "sections": {{"Experience": true, "Education": true, "Projects": true, "Certifications": false, "Skills": true}},
    "skills": ["Skill1", "Skill2", "Skill3"],
    "ats_score": {ats_score},
    "formatting_score": {formatting_score},
    "impact_score": {impact_score},
    "clarity_score": {clarity_score},
    "strengths": ["Strength 1", "Strength 2", "Strength 3"],
    "areas_for_improvement": ["1. Improvement One", "2. Improvement Two", "3. Improvement Three"],
    "role_suggestions": ["Role 1", "Role 2", "Role 3", "Role 4", "Role 5", "Role 6"],
    "missing_keywords": ["Keyword 1", "Keyword 2", "Keyword 3", "Keyword 4"]
}}
"""
        
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json", "max_output_tokens": 600, "temperature": 0.2},
            request_options={"timeout": 5.0}
        )

        if response and response.text:
            parsed = json.loads(response.text)
            for k, v in fallback_analysis.items():
                if k not in parsed:
                    parsed[k] = v
                    
            # CRITICAL: Always use our deterministic heuristic ATS score (already normalized to integer)
            # This ensures PDF and DOCX of the same resume always show the SAME score
            parsed['ats_score'] = ats_score  # integer from calculate_ats_score
            parsed['formatting_score'] = max(10, min(_safe_int(parsed.get('formatting_score'), formatting_score), 100))
            parsed['impact_score'] = max(10, min(_safe_int(parsed.get('impact_score'), impact_score), 100))
            parsed['clarity_score'] = max(10, min(_safe_int(parsed.get('clarity_score'), clarity_score), 100))
            
            if not parsed.get('skills') or not isinstance(parsed.get('skills'), list):
                parsed['skills'] = extracted_skills

            # SAFETY: Always use skill-accurate smart_roles for role_suggestions
            # This prevents AI hallucination (e.g. React roles when resume has no React)
            skill_set_lower = {s.lower() for s in extracted_skills}
            has_react_in_resume = any(s in skill_set_lower for s in ['react', 'react.js', 'react native'])

            ai_roles = parsed.get('role_suggestions', [])
            # Filter out any React roles hallucinated by AI if react is not in the resume
            if not has_react_in_resume:
                ai_roles = [r for r in ai_roles if 'react' not in r.lower()]

            # Use smart_roles if AI gave too few, OR always prefer smart_roles (more accurate)
            if not ai_roles or len(ai_roles) < 4:
                parsed['role_suggestions'] = smart_roles
            else:
                # Merge: smart_roles first (accurate), then any non-React AI roles not already covered
                seen_lower = {r.lower() for r in smart_roles}
                merged = list(smart_roles)
                for r in ai_roles:
                    if r.lower() not in seen_lower and len(merged) < 7:
                        merged.append(r)
                        seen_lower.add(r.lower())
                parsed['role_suggestions'] = merged[:6]

            return parsed
    except Exception as e:
        print(f"Error in analyze_resume_with_ai (using fast fallback): {e}")

    return fallback_analysis
