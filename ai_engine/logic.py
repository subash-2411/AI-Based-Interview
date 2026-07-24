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
    'HR': [
        "உங்கள பத்தியும் உங்க background பத்தியும் சொல்லுங்க.",
        "நாங்க ஏன் உங்கள இந்த role-க்கு hire பண்ணனும்?",
        "உங்க strengths மற்றும் weaknesses என்ன?",
        "Next 5 years-ல உங்கள எங்க பாக்குறீங்க?",
        "ஒரு team environment-ல conflicts-ஐ எப்படி handle பண்ணுவீங்க?",
        "உங்க career-ல நீங்க face பண்ண ஒரு difficult challenge பத்தி சொல்லுங்க."
    ]
}

def generate_questions(skills, count=5, language='en-US', difficulty='Intermediate'):
    # Normalize skills
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',') if s.strip()]
    if not skills:
        skills = ['Python', 'SQL', 'Django']

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            skill_str = ", ".join(skills)
            
            prompt = f"You are an expert technical interviewer. The candidate's resume highlights the following skills: {skill_str}. "
            prompt += f"Generate exactly {count} unique, non-repeating interview questions STRICTLY based on these specific skills. Do NOT ask questions about technologies not listed here. "
            
            if difficulty.lower() == 'beginner':
                prompt += "Keep the questions VERY SIMPLE, short, and direct. Ask basic foundational questions (e.g., 'What is...', 'Explain the difference between...'). Avoid long scenario-based questions. "
            elif difficulty.lower() == 'intermediate':
                prompt += "Keep the questions moderately difficult but CONCISE. Ask a mix of theory and simple practical applications. Do not write overly long scenarios. "
            else:
                prompt += "Ask complex, in-depth, scenario-based, or architectural questions suitable for an advanced professional. The questions can be detailed. "
            
            if language == 'ta-IN':
                prompt += "Provide the questions translated into formal Tamil. Ensure EVERY single question is written strictly in formal Tamil script."
            elif language == 'ta-EN':
                prompt += "Provide the questions translated into Tanglish (Tamil written in English/Latin script). Tanglish is a blend of Tamil and English, using Latin characters (e.g., 'Python-ல Decorators-னா என்ன, அது ஏன் use பண்றாங்க?', 'உங்கள பத்தியும் உங்க background பத்தியும் சொல்லுங்க.'). Keep technical terms in English but write the surrounding sentence structure and connecting words in Tamil written with Latin characters. Ensure EVERY single question is strictly in Tanglish. Do NOT write any questions in pure English or pure Tamil script."
            else:
                prompt += "Provide the questions in English. Ensure EVERY single question is strictly in English."
                
            prompt += " Format the output as a simple list of questions, one per line. Do NOT include numbers, bullet points, asterisks, or intro/outro text. Just the questions. Each question must be highly concise, limited to a maximum of 2 short sentences and under 30 words total, so it is fully readable on screen."
            
            response = model.generate_content(prompt, request_options={"timeout": 15.0})
            
            # Parse response
            raw_questions = [q.strip() for q in response.text.strip().split('\n') if q.strip()]
            cleaned_questions = [re.sub(r'^[\d\.\-\*\s]+', '', q).strip() for q in raw_questions]
            
            if len(cleaned_questions) >= count:
                return cleaned_questions[:count]
            elif cleaned_questions:
                # If we got fewer than requested, pad with fallback
                fallback_needed = count - len(cleaned_questions)
                fallback_qs = get_fallback_questions(skills, fallback_needed, language)
                return cleaned_questions + fallback_qs
        except Exception as e:
            print(f"Gemini generation failed: {e}")
            pass # Fallback below
            
    return get_fallback_questions(skills, count, language)

def get_fallback_questions(skills, count=5, language='en-US'):
    # Normalize skills
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',') if s.strip()]
    if not skills:
        skills = ['Python', 'SQL', 'Django']

    questions = []
    if language == 'ta-IN':
        bank = QUESTION_BANK_TAMIL
    elif language == 'ta-EN':
        bank = QUESTION_BANK_TANGLISH
    else:
        bank = QUESTION_BANK
    
    # Always include HR
    questions.extend(random.sample(bank['HR'], min(2, len(bank['HR']))))
    
    # Include Technical based on skills
    found_tech = False
    for skill in skills:
        if skill in bank:
            questions.extend(random.sample(bank[skill], min(2, len(bank[skill]))))
            found_tech = True
            
    # Fallback if no skills matched or we need more questions
    if len(questions) < count:
        # Try to fill with other technical questions first
        tech_categories = [k for k in bank.keys() if k != 'HR']
        random.shuffle(tech_categories)
        for cat in tech_categories:
            if len(questions) >= count:
                break
            available_qs = list(set(bank[cat]) - set(questions))
            if available_qs:
                needed = count - len(questions)
                questions.extend(random.sample(available_qs, min(needed, 2)))

    # Fallback to HR questions if we still don't have enough
    if len(questions) < count:
        remaining = count - len(questions)
        available_hr = list(set(bank['HR']) - set(questions))
        if available_hr:
            questions.extend(random.sample(available_hr, min(remaining, len(available_hr))))
        
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
    """Provides a helpful hint to the user based on their current code."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "API Key missing. Cannot provide hints."
        
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        You are an expert, friendly, and encouraging AI coding tutor.
        The student has ABSOLUTE ZERO CODING KNOWLEDGE (a complete beginner). You must guide them step-by-step and provide the full code solution.
        
        The student is trying to solve this problem:
        Title: {problem_title}
        Description: {problem_desc}
        
        This is their current code:
        {user_code}
        """
        
        if language == 'ta-EN':
            prompt += """
            Use simple, encouraging, and clear language. You MUST explain the concepts and lines in Tanglish (easy-to-understand English mixed with Tamil, e.g. "Intha problem-la loop use panni run pannanum", "line 3-la empty list template target variable match panni compare panrom", etc.).
            
            You MUST provide:
            1. The **FULL COMPLETED SOLUTION CODE** FIRST, so the student can see exactly how it should be written.
            2. A **simple, step-by-step line-by-line explanation** of that code in friendly Tanglish/English.
            3. Explain what each line does conceptually (e.g., what variables, lists, dicts, or loops do in simple terms).
            """
        else:
            prompt += """
            Use simple, encouraging, and clear language. You MUST explain the concepts and lines strictly in English.
            
            You MUST provide:
            1. The **FULL COMPLETED SOLUTION CODE** FIRST, so the student can see exactly how it should be written.
            2. A **simple, step-by-step line-by-line explanation** of that code in friendly, basic English.
            3. Explain what each line does conceptually (e.g., what variables, lists, dicts, or loops do in simple terms).
            """
            
        response = model.generate_content(prompt, request_options={"timeout": 60.0})
        return response.text.strip()
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        try:
            with open("scratch/gemini_hint_error.log", "w") as f:
                f.write(f"Exception in get_coding_hint:\n{tb}\n")
        except:
            pass
        print(f"Error getting hint: {e}")
        return "I'm having trouble analyzing your code right now. Make sure your syntax is mostly correct and try again!"

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


