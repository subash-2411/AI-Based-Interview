import random
import os
import re
from dotenv import load_dotenv

load_dotenv()

QUESTION_BANK = {
    'Python': [
        "What are decorators in Python and why are they used?",
        "Explain the difference between list and tuple with use cases.",
        "What is PEP 8 and why is it important?",
        "How is memory managed in Python? Explain Garbage Collection.",
        "What are generators and how do they differ from iterators?",
        "Explain the concept of GIL (Global Interpreter Lock)."
    ],
    'Django': [
        "What is the MVT pattern in Django? How is it different from MVC?",
        "Explain Django Middleware and its lifecycle.",
        "What are signals in Django? Give a real-world example.",
        "How do you handle database migrations in Django?",
        "Explain the role of Django Rest Framework (DRF) in building APIs.",
        "How do you handle authentication in Django projects?"
    ],
    'React': [
        "What are Hooks in React? Explain useEffect.",
        "Difference between Functional and Class components.",
        "What is Virtual DOM and how does it work?",
        "Explain State vs Props in React.",
        "How do you handle API calls in a React application?",
        "What is Redux and when should we use it?"
    ],
    'Java': [
        "Explain the concept of OOPs in Java.",
        "Difference between Abstract Class and Interface.",
        "What is Spring Boot and why is it popular?",
        "Explain Exception Handling in Java.",
        "What is Hibernate and how does it relate to ORM?",
        "Explain Multithreading in Java."
    ],
    'SQL': [
        "Difference between INNER JOIN, LEFT JOIN, and RIGHT JOIN.",
        "Explain Database Normalization (1NF, 2NF, 3NF).",
        "What are Primary Keys, Foreign Keys, and Unique Keys?",
        "How do you optimize a slow SQL query?",
        "What is an Index in SQL and how does it improve performance?",
        "Explain the ACID properties in database transactions."
    ],
    'Accounting': [
        "Explain the 3 Golden Rules of Accounting with examples.",
        "What is the difference between Trial Balance and Balance Sheet?",
        "Explain the concept of Bank Reconciliation Statement (BRS).",
        "What are the different types of GST (CGST, SGST, IGST) and how are they applied?",
        "What is the difference between Accrual Accounting and Cash Accounting?",
        "How do you calculate and analyze Working Capital in a business?"
    ],
    'Finance': [
        "Explain the difference between Cash Flow and Fund Flow statements.",
        "What is EBITDA and why is it an important metric for evaluating businesses?",
        "How do you evaluate capital budgeting decisions using Net Present Value (NPV) and IRR?",
        "What is Depreciation and what are the main methods of calculating it?",
        "Explain the concept of Debt-to-Equity Ratio and its significance."
    ],
    'Operations': [
        "How do you manage inventory levels using Economic Order Quantity (EOQ) or JIT?",
        "Explain how you handle vendor management and resolve vendor delivery delays.",
        "What KPIs do you track to measure daily operational efficiency?",
        "How do you handle unexpected workflow bottlenecks in a high-pressure environment?"
    ],
    'HR': [
        "Tell me about yourself and your background.",
        "Why should we hire you for this role?",
        "What are your greatest strengths and weaknesses?",
        "Where do you see yourself in the next 5 years?",
        "How do you handle conflict in a team environment?",
        "Tell me about a time you faced a difficult challenge at work/college."
    ]
}

QUESTION_BANK_TAMIL = {
    'Python': [
        "பைத்தானில் டெக்கரேட்டர்கள் (Decorators) என்றால் என்ன, அவை ஏன் பயன்படுத்தப்படுகின்றன?",
        "List மற்றும் Tuple இடையிலான வித்தியாசத்தை தகுந்த உதாரணங்களுடன் விளக்குங்கள்.",
        "PEP 8 என்றால் என்ன மற்றும் அது ஏன் முக்கியமானது?",
        "பைத்தானில் மெமரி மேனேஜ்மென்ட் எப்படி செய்யப்படுகிறது? கார்பேஜ் கலெக்ஷன் (Garbage Collection) பற்றி விளக்குங்கள்.",
        "Generators என்றால் என்ன மற்றும் அவை Iterators-லிருந்து எப்படி வேறுபடுகின்றன?",
        "GIL (Global Interpreter Lock) என்ற கருத்தை விளக்குங்கள்."
    ],
    'Django': [
        "Django-வில் MVT பேட்டர்ன் என்றால் என்ன? இது MVC-யிலிருந்து எப்படி வேறுபடுகிறது?",
        "Django Middleware மற்றும் அதன் வாழ்க்கைச் சுழற்சி (Lifecycle) பற்றி விளக்குங்கள்.",
        "Django-வில் Signals என்றால் என்ன? ஒரு நிஜ கால உதாரணத்தைக் கூறுங்கள்.",
        "Django-வில் டேட்டாபேஸ் மைக்ரேஷன்களை (Migrations) எப்படி கையாள்வீர்கள்?",
        "API-களை உருவாக்குவதில் Django Rest Framework (DRF)-ன் பங்கு என்ன?",
        "Django புராஜெக்ட்களில் அத்தென்டிகேஷன் (Authentication) முறையை எப்படி கையாள்வீர்கள்?"
    ],
    'React': [
        "React-ல் Hooks என்றால் என்ன? useEffect பற்றி விளக்குங்கள்.",
        "Functional மற்றும் Class கூறுகளுக்கு (Components) இடையிலான வித்தியாசம் என்ன?",
        "Virtual DOM என்றால் என்ன மற்றும் அது எப்படி வேலை செய்கிறது?",
        "React-ல் State மற்றும் Props இடையிலான வித்தியாசத்தை விளக்குங்கள்.",
        "React அப்ளிகேஷனில் API கால்களை (Calls) எப்படி கையாள்வீர்கள்?",
        "Redux என்றால் என்ன மற்றும் அதை எப்போது பயன்படுத்த வேண்டும்?"
    ],
    'Java': [
        "ஜாவாவில் OOPs என்ற கருத்தை விளக்குங்கள்.",
        "Abstract Class மற்றும் Interface இடையிலான வித்தியாசம் என்ன?",
        "Spring Boot என்றால் என்ன மற்றும் அது ஏன் பிரபலமானது?",
        "ஜாவாவில் எக்ஸெப்ஷன் ஹேண்ட்லிங் (Exception Handling) பற்றி விளக்குங்கள்.",
        "Hibernate என்றால் என்ன மற்றும் அது ORM-உடன் எப்படி தொடர்புடையது?",
        "ஜாவாவில் மல்டித்ரெடிங் (Multithreading) பற்றி விளக்குங்கள்."
    ],
    'SQL': [
        "INNER JOIN, LEFT JOIN மற்றும் RIGHT JOIN இடையிலான வித்தியாசம் என்ன?",
        "டேட்டாபேஸ் நார்மலைசேஷன் (1NF, 2NF, 3NF) பற்றி விளக்குங்கள்.",
        "Primary Keys, Foreign Keys மற்றும் Unique Keys என்றால் என்ன?",
        "SQL Query-ஐ எப்படி ஆப்டிமைஸ் செய்வது?",
        "SQL-ல் Index என்றால் என்ன மற்றும் அது செயல்திறனை (Performance) எப்படி மேம்படுத்துகிறது?",
        "டேட்டாபேஸ் டிரான்சாக்ஷன்களில் ACID பண்புகளை விளக்குங்கள்."
    ],
    'Accounting': [
        "கணக்கியலின் 3 பொன் விதிகளை (3 Golden Rules of Accounting) உதாரணங்களுடன் விளக்குங்கள்.",
        "இருப்பாய்வு (Trial Balance) மற்றும் இருப்புநிலைக் குறிப்பு (Balance Sheet) இடையிலான வித்தியாசம் என்ன?",
        "வங்கி சமரசப் பட்டியல் (Bank Reconciliation Statement - BRS) என்றால் என்ன?",
        "ஜிஎஸ்டி (GST) பிரிவுகள் (CGST, SGST, IGST) எவ்வாறு கணக்கிடப்படுகின்றன?"
    ],
    'HR': [
        "உங்களைப் பற்றியும் உங்கள் பின்னணியைப் பற்றியும் சொல்லுங்கள்.",
        "நாங்கள் ஏன் உங்களை இந்த வேலைக்கு அமர்த்த வேண்டும்?",
        "உங்கள் பலம் மற்றும் பலவீனங்கள் என்ன?",
        "அடுத்த 5 ஆண்டுகளில் உங்களை எங்கே பார்க்கிறீர்கள்?",
        "ஒரு குழு சூழலில் நீங்கள் மோதல்களை (Conflicts) எப்படி கையாள்வீர்கள்?",
        "வேலையில் அல்லது கல்லூரியில் நீங்கள் சந்தித்த ஒரு கடினமான சவாலைப் பற்றி சொல்லுங்கள்."
    ]
}

QUESTION_BANK_TANGLISH = {
    'Python': [
        "Python-ல Decorators-னா என்ன, அது ஏன் use பண்றாங்க?",
        "List-க்கும் Tuple-க்கும் இருக்குற difference-ஐ examples-ஓட explain பண்ணுங்க.",
        "PEP 8-ன்னா என்ன? அது ஏன் important?",
        "Python-ல memory management எப்படி நடக்குது? Garbage Collection பத்தி சொல்லுங்க.",
        "Generators-னா என்ன? அது iterators-ல இருந்து எப்படி differ ஆகுது?",
        "GIL (Global Interpreter Lock) concept-ஐ explain பண்ணுங்க."
    ],
    'Django': [
        "Django-ல MVT pattern-னா என்ன? இது MVC-ல இருந்து எப்படி different?",
        "Django Middleware மற்றும் அதோட lifecycle பத்தி சொல்லுங்க.",
        "Django-ல Signals-னா என்ன? ஒரு real-world example குடுங்க.",
        "Django migrations-ஐ எப்படி handle பண்ணுவீங்க?",
        "APIs build பண்ணும்போது Django Rest Framework (DRF)-ஓட role என்ன?",
        "Django projects-ல authentication-ஐ எப்படி handle பண்ணுவீங்க?"
    ],
    'React': [
        "React Hooks-னா என்ன? useEffect பத்தி explain பண்ணுங்க.",
        "Functional மற்றும் Class components-க்கு இருக்குற difference என்ன?",
        "Virtual DOM-னா என்ன? அது எப்படி work ஆகுது?",
        "React-ல State vs Props difference சொல்லுங்க.",
        "React app-ல API calls எப்படி handle பண்ணுவீங்க?",
        "Redux-னா என்ன? அதை எப்போ use பண்ணனும்?"
    ],
    'Java': [
        "Java-ல OOPs concepts-ஐ explain பண்ணுங்க.",
        "Abstract Class-க்கும் Interface-க்கும் இருக்குற difference என்ன?",
        "Spring Boot ஏன் இவ்ளோ popular-ஆ இருக்கு?",
        "Java-ல Exception Handling பத்தி explain பண்ணுங்க.",
        "Hibernate-னா என்ன? அது ORM-கூட எப்படி relate ஆகுது?",
        "Java multithreading பத்தி சொல்லுங்க."
    ],
    'SQL': [
        "INNER JOIN, LEFT JOIN மற்றும் RIGHT JOIN difference என்ன?",
        "Database Normalization (1NF, 2NF, 3NF) பத்தி explain பண்ணுங்க.",
        "Primary Keys மற்றும் Foreign Keys-னா என்ன?",
        "ஒரு slow SQL query-ஐ எப்படி optimize பண்ணுவீங்க?",
        "SQL-ல Index-னா என்ன? அது performance-ஐ எப்படி improve பண்ணுது?",
        "Database transactions-ல ACID properties-ஐ explain பண்ணுங்க."
    ],
    'Accounting': [
        "Accounting-ல இருக்குற 3 Golden Rules-ஐ examples-ஓட explain பண்ணுங்க.",
        "Trial Balance-க்கும் Balance Sheet-க்கும் இருக்குற main difference என்ன?",
        "Bank Reconciliation Statement (BRS) எப்போ create பண்ணுவாங்க?",
        "GST-ல CGST, SGST, IGST எப்போ apply பண்ணுவாங்க?",
        "Working Capital-னா என்ன? அதை எப்படி calculate பண்ணுவீங்க?"
    ],
    'HR': [
        "உங்கள பத்தியும் உங்க background பத்தியும் சொல்லுங்க.",
        "நாங்க ஏன் உங்கள இந்த role-க்கு hire பண்ணனும்?",
        "உங்க strengths மற்றும் weaknesses என்ன?",
        "Next 5 years-ல உங்கள எங்க பாக்குறீங்க?",
        "ஒரு team environment-ல conflicts-ஐ எப்படி handle பண்ணுவீங்க?",
        "உங்க career-ல நீங்க face பண்ண ஒரு difficult challenge பத்தி சொல்லுங்க."
    ]
}

def non_it_keywords_from_text(resume_text):
    """
    When resume.skills is empty (no SKILL_DB match), extract domain keywords
    from the raw resume text using degree and job title patterns.
    Returns a list of domain-relevant skill strings for question generation.
    """
    text_lower = resume_text.lower()
    extracted = []

    # Degree detection
    degree_map = [
        (['b.com', 'bcom', 'bachelor of commerce', 'b.com.', 'b com'], ['Financial Accounting', 'GST', 'Tally', 'Taxation']),
        (['m.com', 'mcom', 'master of commerce'], ['Financial Accounting', 'Cost Accounting', 'GST', 'Auditing']),
        (['mba', 'm.b.a', 'master of business'], ['Business Development', 'Sales', 'Operations Management', 'HR Operations']),
        (['bba', 'b.b.a', 'bachelor of business'], ['Business Development', 'Sales', 'CRM']),
        (['b.sc accounting', 'accounting and finance'], ['Financial Accounting', 'Bookkeeping', 'Auditing']),
    ]
    for keywords, skills in degree_map:
        if any(k in text_lower for k in keywords):
            extracted.extend(skills)

    # Job title / domain detection from text
    domain_title_map = [
        (['accountant', 'accounts executive', 'audit', 'accounts assistant', 'finance executive'], ['Financial Accounting', 'Tally', 'GST', 'Bookkeeping', 'Bank Reconciliation']),
        (['hr executive', 'hr manager', 'human resources', 'recruiter', 'talent acquisition'], ['Human Resources', 'Recruitment', 'Payroll Management', 'Employee Relations']),
        (['sales executive', 'sales manager', 'business development'], ['Sales', 'Business Development', 'CRM', 'Lead Generation']),
        (['digital marketing', 'seo specialist', 'content writer', 'marketing executive'], ['Digital Marketing', 'SEO', 'Content Marketing']),
        (['operations', 'supply chain', 'logistics', 'procurement'], ['Operations Management', 'Vendor Management']),
    ]
    for keywords, skills in domain_title_map:
        if any(k in text_lower for k in keywords):
            extracted.extend(skills)

    # Direct non-IT skill keyword presence in raw text
    direct_non_it = [
        'tally', 'gst', 'taxation', 'auditing', 'bookkeeping', 'ledger',
        'payroll', 'bank reconciliation', 'balance sheet', 'trial balance',
        'sap fico', 'quickbooks', 'zoho books', 'vlookup', 'pivot tables',
        'mis report', 'accounts payable', 'accounts receivable'
    ]
    for kw in direct_non_it:
        if kw in text_lower and kw.title() not in extracted:
            extracted.append(kw.title())

    # Deduplicate
    seen = set()
    result = []
    for s in extracted:
        if s.lower() not in seen:
            seen.add(s.lower())
            result.append(s)

    return result if result else []


def _detect_domain(skills, resume_text=''):
    """
    Returns (is_non_tech, domain_area, domain_key) based on skills list.
    Uses word-boundary matching to avoid false positives like 'ai' in 'email'.
    """
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',') if s.strip()]

    # Build a set of exact lowercase skill names for precise matching
    skill_set = {s.strip().lower() for s in skills}

    # Non-IT / Commerce / Business skill indicators (exact match)
    non_tech_exact = {
        'tally', 'tally prime', 'tally erp', 'gst', 'gst filing', 'tds',
        'accounting', 'financial accounting', 'cost accounting', 'management accounting',
        'auditing', 'taxation', 'ledger', 'balance sheet', 'trial balance', 'bookkeeping',
        'brs', 'bank reconciliation', 'accounts payable', 'accounts receivable',
        'payroll management', 'payroll', 'vlookup', 'pivot tables', 'mis reporting',
        'sap fico', 'quickbooks', 'zoho books', 'advanced excel',
        'human resources', 'hr operations', 'talent acquisition', 'recruitment',
        'employee relations', 'performance management',
        'business development', 'sales', 'lead generation', 'client relations',
        'digital marketing', 'seo', 'content marketing',
        'operations management', 'vendor management',
        'mba', 'bba', 'b.com', 'crm'
    }

    # Core IT / Programming skill indicators (exact match - no substring)
    tech_exact = {
        'python', 'java', 'react', 'react.js', 'c++', 'c#', 'django', 'flask', 'fastapi',
        'javascript', 'typescript', 'node.js', 'express', 'flutter', 'kotlin', 'swift',
        'golang', 'go', 'php', 'ruby', 'rust', '.net', 'asp.net', 'spring', 'spring boot',
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
        'artificial intelligence', 'nlp', 'natural language processing', 'computer vision',
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'google cloud',
        'react native', 'angular', 'vue', 'vue.js', 'next.js', 'tailwindcss',
        'scikit-learn', 'langchain', 'openai', 'huggingface'
    }
    # Note: 'excel', 'github', 'git', 'sql', 'mysql', 'html', 'css' are ambiguous
    # (used by both IT and non-IT) — do NOT put them in tech_exact

    has_non_tech = bool(skill_set & non_tech_exact)
    has_tech = bool(skill_set & tech_exact)

    # Also check raw resume text for degree/education if skills alone are inconclusive
    if resume_text and not has_non_tech and not has_tech:
        text_lower = resume_text.lower()
        degree_indicators = ['b.com', 'bcom', 'mba', 'bba', 'm.com', 'mcom', 'bachelor of commerce',
                             'master of business', 'accountant', 'accounts executive', 'audit',
                             'hr executive', 'human resources', 'sales executive', 'digital marketing',
                             'tally', 'gst', 'taxation', 'bookkeeping', 'payroll']
        it_indicators = ['computer science', 'b.e', 'b.tech', 'btech', 'software engineer',
                         'full stack', 'backend developer', 'frontend developer', 'python developer']
        text_has_non_it = any(d in text_lower for d in degree_indicators)
        text_has_it = any(i in text_lower for i in it_indicators)
        if text_has_non_it and not text_has_it:
            has_non_tech = True
    elif resume_text and has_non_tech and not has_tech:
        # Confirm no IT degree in resume text even if skills look non-IT
        text_lower = resume_text.lower()
        it_indicators = ['computer science', 'b.e', 'b.tech', 'btech', 'software engineer',
                         'full stack', 'python developer', 'java developer']
        if any(i in text_lower for i in it_indicators):
            has_tech = True  # override — IT resume
    # Determine domain
    if has_non_tech and not has_tech:
        # Pure Non-IT
        if skill_set & {'tally', 'tally prime', 'tally erp', 'gst', 'gst filing', 'tds',
                        'accounting', 'financial accounting', 'cost accounting', 'auditing',
                        'taxation', 'ledger', 'balance sheet', 'trial balance', 'bookkeeping',
                        'brs', 'bank reconciliation', 'sap fico', 'quickbooks', 'zoho books'}:
            return True, "Accounting, Financial Statements, GST/TDS filing, Tally, Bank Reconciliation, Balance Sheet", "Accounting"
        elif skill_set & {'human resources', 'hr operations', 'talent acquisition', 'recruitment',
                          'employee relations', 'performance management', 'payroll', 'payroll management'}:
            return True, "HR Operations, Recruitment, Talent Acquisition, Payroll, Employee Relations", "HR"
        elif skill_set & {'sales', 'business development', 'lead generation', 'client relations', 'crm'}:
            return True, "Sales strategies, Client Relations, CRM tools, Lead Generation, Business Development", "HR"
        elif skill_set & {'digital marketing', 'seo', 'content marketing'}:
            return True, "Digital Marketing, SEO, Content Strategy, Social Media, Campaign Analytics", "HR"
        elif skill_set & {'operations management', 'vendor management'}:
            return True, "Operations Management, Vendor Relationships, Supply Chain, Process Optimization", "Operations"
        else:
            return True, "Business operations, Professional communication, Problem-solving", "HR"

    # Pure IT or mixed (IT skills present) → treat as IT
    return False, None, None


def generate_questions(skills, count=5, language='en-US', difficulty='Beginner', company='General', resume_text=''):
    # Normalize skills
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',') if s.strip()]
    if not skills:
        skills = []

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    # Detect domain — pass resume_text for degree-based detection
    is_non_tech, domain_area, domain_key = _detect_domain(skills, resume_text=resume_text)

    # If non-IT but no skills extracted, derive from resume text
    if is_non_tech and not skills and resume_text:
        skills = non_it_keywords_from_text(resume_text) or ['Financial Accounting', 'GST', 'Tally']
    elif not skills:
        # Last fallback — general professional
        skills = ['Communication', 'Problem Solving', 'Time Management']

    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            skill_str = ", ".join(skills)

            if is_non_tech:
                domain_desc = (
                    f"The candidate has a NON-IT / Commerce / Business background with skills: {skill_str}. "
                    f"Generate interview questions STRICTLY about: {domain_area}. "
                    f"IMPORTANT: DO NOT ask any programming, coding, software, or IT questions. "
                    f"Only ask domain-specific professional questions."
                )
            else:
                domain_desc = (
                    f"The candidate has a Technical software background with skills: {skill_str}. "
                    f"Generate technical interview questions covering these specific technologies."
                )

            prompt = f"You are an expert interviewer. {domain_desc} "
            if company and company != 'General':
                prompt += f"Interview is for {company}. Tailor context slightly if possible. "

            prompt += f"Generate exactly {count} unique, non-repeating interview questions STRICTLY based on these skills. "

            if difficulty.lower() == 'beginner':
                prompt += "Keep questions VERY SIMPLE and direct. Ask basic foundational questions ('What is...', 'Explain the difference between...'). "
            elif difficulty.lower() == 'intermediate':
                prompt += "Moderately difficult, mix of theory and practical. Concise, no long scenarios. "
            else:
                prompt += "In-depth, scenario-based questions for experienced professionals. "

            if language == 'ta-IN':
                prompt += "Translate questions into formal Tamil script."
            elif language == 'ta-EN':
                prompt += "Write in Tanglish (Tamil + English blend). Keep technical terms in English, connectors in Tamil-English."
            else:
                prompt += "Write in clear English."

            prompt += " Format: one question per line, no numbers or bullet points, each under 30 words."

            response = model.generate_content(prompt, request_options={"timeout": 12.0})

            raw_questions = [q.strip() for q in response.text.strip().split('\n') if q.strip()]
            cleaned_questions = [re.sub(r'^[\d\.\-\*\s]+', '', q).strip() for q in raw_questions]

            if len(cleaned_questions) >= count:
                return cleaned_questions[:count]
            elif cleaned_questions:
                fallback_needed = count - len(cleaned_questions)
                fallback_qs = get_fallback_questions(skills, fallback_needed, language, is_non_tech=is_non_tech, domain_key=domain_key)
                return cleaned_questions + fallback_qs
        except Exception as e:
            print(f"Gemini question generation failed: {e}")

    return get_fallback_questions(skills, count, language, is_non_tech=is_non_tech, domain_key=domain_key)


def get_fallback_questions(skills, count=5, language='en-US', is_non_tech=None, domain_key=None):
    # Normalize skills
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',') if s.strip()]
    if not skills:
        skills = ['Python', 'SQL', 'Django']

    # Auto-detect if not passed
    if is_non_tech is None:
        is_non_tech, _, domain_key = _detect_domain(skills)

    questions = []
    if language == 'ta-IN':
        bank = QUESTION_BANK_TAMIL
    elif language == 'ta-EN':
        bank = QUESTION_BANK_TANGLISH
    else:
        bank = QUESTION_BANK

    # Always include 2 HR questions
    questions.extend(random.sample(bank['HR'], min(2, len(bank['HR']))))

    if is_non_tech:
        # Non-IT: pull from Accounting, Finance, Operations — never from Python/Java/React
        non_it_categories = []
        if domain_key and domain_key in bank:
            non_it_categories.append(domain_key)
        # Always supplement with available non-IT banks
        for cat in ['Accounting', 'Finance', 'Operations']:
            if cat in bank and cat not in non_it_categories:
                non_it_categories.append(cat)

        for cat in non_it_categories:
            if len(questions) >= count:
                break
            avail = list(set(bank.get(cat, [])) - set(questions))
            if avail:
                needed = min(count - len(questions), 3)
                questions.extend(random.sample(avail, min(needed, len(avail))))
    else:
        # IT: match skills to question bank categories
        skill_set = {s.strip().lower() for s in skills}
        it_categories = ['Python', 'Django', 'React', 'Java', 'SQL']
        matched = False

        for cat in it_categories:
            if cat.lower() in skill_set and cat in bank:
                avail = list(set(bank[cat]) - set(questions))
                if avail:
                    questions.extend(random.sample(avail, min(2, len(avail))))
                    matched = True

        # If nothing matched, fill from all IT categories
        if not matched or len(questions) < count:
            it_cats = [k for k in bank.keys() if k not in ('HR', 'Accounting', 'Finance', 'Operations')]
            random.shuffle(it_cats)
            for cat in it_cats:
                if len(questions) >= count:
                    break
                avail = list(set(bank[cat]) - set(questions))
                if avail:
                    questions.extend(random.sample(avail, min(2, len(avail))))

    # Fill remaining with HR if still short
    if len(questions) < count:
        remaining = count - len(questions)
        avail_hr = list(set(bank['HR']) - set(questions))
        if avail_hr:
            questions.extend(random.sample(avail_hr, min(remaining, len(avail_hr))))

    random.shuffle(questions)
    return questions[:count]


FALLBACK_CODING_PROBLEMS = {
    'Python': [
        {
            "title": "Python Two Sum",
            "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nExample:\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]",
            "difficulty": "Easy",
            "tags": "Python, Array, Logic",
            "language": "Python",
            "initial_code": "def solution(nums, target):\n    # Write your code here\n    pass"
        },
        {
            "title": "Python Reverse String",
            "description": "Write a function that reverses a string. The input string is given as an array of characters s.\n\nExample:\nInput: s = ['h','e','l','l','o']\nOutput: ['o','l','l','e','h']",
            "difficulty": "Easy",
            "tags": "Python, String, Array",
            "language": "Python",
            "initial_code": "def solution(s):\n    # Write your code here\n    pass"
        }
    ],
    'General': [
        {
            "title": "General FizzBuzz",
            "description": "Write a program that outputs the string representation of numbers from 1 to n. But for multiples of three it should output 'Fizz' instead of the number and for the multiples of five output 'Buzz'. For numbers which are multiples of both three and five output 'FizzBuzz'.",
            "difficulty": "Easy",
            "tags": "General, Logic, Math",
            "language": "Python",
            "initial_code": "def solution(n):\n    # Write your code here\n    pass"
        },
        {
            "title": "General Palindrome Check",
            "description": "Given an integer x, return true if x is a palindrome, and false otherwise.\n\nExample:\nInput: x = 121\nOutput: true",
            "difficulty": "Easy",
            "tags": "General, Math, Logic",
            "language": "Python",
            "initial_code": "def solution(x):\n    # Write your code here\n    pass"
        }
    ]
}

def get_coding_hint(problem_title, problem_desc, user_code, language='ta-EN'):
    """Provides a fast, helpful hint and solution breakdown to the user."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    
    if api_key:
        try:
            import google.generativeai as genai
            clean_keys = [k.strip() for k in api_key.split(',') if k.strip()]
            if clean_keys:
                genai.configure(api_key=clean_keys[0])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                lang_instruction = "Explain in Tanglish (Tamil + English blend, simple and encouraging words)." if language == 'ta-EN' else "Explain in concise, encouraging English."
                
                prompt = f"""
                You are a fast, friendly AI coding tutor.
                Problem: {problem_title}
                Details: {problem_desc[:300]}
                Student Code:
                {user_code[:400] if user_code else 'No code written yet'}

                Task:
                1. Give the exact solution code (short and clean).
                2. Explain the 2-3 key steps simply ({lang_instruction}).
                Keep the response concise and direct (under 180 words).
                """
                
                response = model.generate_content(
                    prompt,
                    generation_config={"max_output_tokens": 400, "temperature": 0.3},
                    request_options={"timeout": 6.0}
                )
                if response and response.text:
                    return response.text.strip()
        except Exception as e:
            print(f"Error in fast Gemini hint: {e}")

    # Instant smart fallback based on language & problem title
    if language == 'ta-EN':
        return f"""💡 **Quick Solution Guide for {problem_title}:**

1. **Approach:** Intha problem-ku core logic approach use pannanum.
2. **Steps:**
   - First, input data-va read panni variables-la store pannunga.
   - Loop or conditions use panni logic check pannunga.
   - Result-ai return or print pannunga.

Keep going! Unga syntax correct-ah irukanu check panni Submit click pannunga."""
    else:
        return f"""💡 **Quick Solution Guide for {problem_title}:**

1. **Approach:** Understand the input/output constraints.
2. **Key Steps:**
   - Initialize the necessary variables or data structures.
   - Iterate through the inputs and apply the condition or transformation.
   - Return or print the expected result.

Review your code structure and click Submit to evaluate!"""

def get_fallback_coding_problems(skills, count=3):
    problems = []
    found_tech = False
    
    # Check for skills in fallback
    for skill in skills:
        for bank_skill in FALLBACK_CODING_PROBLEMS.keys():
            if bank_skill.lower() in skill.lower() or skill.lower() in bank_skill.lower():
                problems.extend(FALLBACK_CODING_PROBLEMS[bank_skill])
                found_tech = True
                
    if not found_tech or len(problems) < count:
        problems.extend(FALLBACK_CODING_PROBLEMS['General'])
        
    random.shuffle(problems)
    return problems[:count]

import json

def generate_coding_problems(resume_text, count=3):
    """Parses resume text to extract skills, then generates coding problems."""
    
    # Try extracting basic skills to use for fallback
    from resume.utils import extract_skills
    skills = extract_skills(resume_text)
    
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        return get_fallback_coding_problems(skills, count)
        
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        You are an expert technical interviewer and coding platform architect.
        I will provide a candidate's resume text.
        Your task is to:
        1. Extract the core programming languages and frameworks from the resume.
        2. Generate exactly {count} unique coding problems tailored to those specific skills.
        
        Resume text:
        {resume_text[:2000]}  # limit text length
        
        Format your response EXACTLY as a JSON array of objects. Do not use markdown code blocks like ```json, just return raw JSON text.
        Each object must have:
        - "title": A short title for the problem (e.g., "React State Counter" or "Python Anagram Checker").
        - "description": A clear description of the problem, what the function should take as input and return as output.
        - "difficulty": "Easy", "Medium", or "Hard".
        - "tags": Comma-separated list of the extracted skills this tests (e.g., "Python, String, Algorithms").
        - "language": The name of the programming language used for the starter code (e.g., "Python", "JavaScript", "Java", "C++").
        - "initial_code": Starter code in the primary language tested.
        """
        
        response = model.generate_content(prompt, request_options={"timeout": 15.0})
        text = response.text.strip()
        
        # Use regex to safely extract JSON array
        import re
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match:
            text = match.group(0)
        else:
            # Fallback in case it returned a single object
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                text = f"[{match.group(0)}]"
                
        problems = json.loads(text)
        return problems
    except Exception as e:
        print(f"Error generating coding problems: {e}")
        return get_fallback_coding_problems(skills, count)


