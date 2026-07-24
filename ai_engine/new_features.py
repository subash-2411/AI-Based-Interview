import json
import os
import re
import traceback
from dotenv import load_dotenv

load_dotenv()

def generate_job_match(resume_text, job_desc):
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return {"match_percentage": 75, "missing_skills": ["Docker", "Kubernetes"], "suggestions": "Add Docker to skills."}
        
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Analyze this Resume against the Job Description.
        Resume: {resume_text[:2000]}
        Job Description: {job_desc[:2000]}
        
        Return ONLY a JSON object with:
        "match_percentage" (int),
        "matching_skills" (list of strings),
        "missing_skills" (list of strings),
        "missing_keywords" (list of strings),
        "ats_compatibility" (string, e.g., "High", "Medium", "Low"),
        "suggestions" (list of strings for improvement).
        Do not include markdown blocks like ```json.
        """
        response = model.generate_content(prompt)
        import re
        text = response.text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match: text = match.group(0)
        return json.loads(text)
    except Exception as e:
        print(f"Error matching job: {e}")
        return {"match_percentage": 70, "missing_skills": ["Failed to analyze"], "suggestions": []}

def predict_salary(skills, experience, location):
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "₹5 LPA - ₹8 LPA"
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"Predict the expected salary range in India (in LPA or ₹ format) for a candidate with skills: {skills}, experience: {experience} years, location: {location}. Return ONLY the salary range as a short string, e.g. '₹12 LPA - ₹18 LPA'."
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return "₹6 LPA - ₹10 LPA"

PREP_FALLBACK_BANK = {
    'zoho': {
        "pattern": "Round 1: Written test (Aptitude & C coding). Round 2: Advanced Programming (Problem solving). Round 3: Technical HR. Round 4: General HR.",
        "skills": ["C Programming", "Data Structures", "Algorithms", "Logical Reasoning"],
        "faqs": [
            "How does memory allocation work in C?",
            "Can you write a program to find all subsets of a set?",
            "Explain the difference between calloc and malloc."
        ],
        "tips": [
            "Focus heavily on string manipulation and array coding problems.",
            "Explain your logic clearly during structural programming rounds.",
            "Brush up on basic aptitude and logic puzzle patterns."
        ]
    },
    'tcs': {
        "pattern": "Round 1: NQT Online Test (Cognitive + Programming). Round 2: Technical Interview. Round 3: Managerial Interview. Round 4: HR Round.",
        "skills": ["Java/Python", "DBMS & SQL", "Software Engineering Concepts", "Data Structures"],
        "faqs": [
            "What are ACID properties in DBMS?",
            "Explain Object Oriented Programming pillars with real examples.",
            "Write a query to find the second highest salary."
        ],
        "tips": [
            "Prepare well for basic coding questions (prime numbers, fibonacci, palindrome).",
            "Be clear about everything you have mentioned in your resume projects.",
            "Practice SQL joins and aggregations."
        ]
    },
    'amazon': {
        "pattern": "Round 1: Online Assessment (Coding + Work Style). Round 2-4: Technical Loops (Coding, System Design, Leadership Principles). Round 5: Bar Raiser.",
        "skills": ["Algorithms & Complex Data Structures", "System Design", "AWS Services", "Leadership Principles"],
        "faqs": [
            "How do you design a rate limiter for APIs?",
            "Implement a thread-safe cache system with eviction policy.",
            "Tell me about a time you had to make a decision without all the data."
        ],
        "tips": [
            "Study Amazon Leadership Principles deeply and frame behavioral answers using STAR.",
            "Practice high-level and low-level system design topics.",
            "Ensure you can talk about the space and time complexity (Big O) of all your code."
        ]
    },
    'google': {
        "pattern": "Round 1: Technical Phone Screen. Round 2-4: Coding Interviews (DSA, Graph, DP). Round 5: System Design. Round 6: Googleyness & Leadership.",
        "skills": ["Advanced Algorithms", "System Design", "Scalability", "Googleyness & Leadership"],
        "faqs": [
            "Given a matrix, find the shortest path from start to end with obstacles.",
            "How do you design a global search indexer like Google Search?",
            "Explain how you would handle conflict within your engineering team."
        ],
        "tips": [
            "Speak your thoughts out loud during the entire coding process.",
            "Focus on clean code, edge case validation, and testing cases.",
            "Deeply understand graphs, recursion, dynamic programming, and heaps."
        ]
    },
    'default': {
        "pattern": "Round 1: Screening Call. Round 2: Technical Assessment. Round 3: Live Coding & System Design. Round 4: Behavioral & HR Interview.",
        "skills": ["Problem Solving", "Core Technology Stack", "System Design", "Communication"],
        "faqs": [
            "What is your approach to debugging complex system issues?",
            "Explain a challenging technical project you worked on recently.",
            "How do you ensure code quality and write test coverage?"
        ],
        "tips": [
            "Be ready to explain the architecture of your past projects clearly.",
            "Ask clarifying questions before writing code in live rounds.",
            "Follow up professionally and show enthusiasm for learning."
        ]
    }
}

def _get_fallback_prep(company_name):
    key = company_name.strip().lower()
    for k, v in PREP_FALLBACK_BANK.items():
        if k in key:
            return v
    return PREP_FALLBACK_BANK['default']

def generate_company_prep_guide(company_name):
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return _get_fallback_prep(company_name)
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""Generate an interview preparation guide for {company_name}.
        Return ONLY a JSON object with:
        "pattern" (string, overview of interview rounds),
        "skills" (list of strings, top skills required),
        "faqs" (list of strings, 3 frequently asked questions),
        "tips" (list of strings, 3 preparation tips).
        """
        response = model.generate_content(prompt)
        import re
        text = response.text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match: text = match.group(0)
        parsed = json.loads(text)
        if "pattern" in parsed:
            return parsed
        return _get_fallback_prep(company_name)
    except:
        return _get_fallback_prep(company_name)

def chat_with_ai_tutor(message, context=""):
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "**Error:** API Key is missing. Please set GEMINI_API_KEY in your .env file."
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""You are a helpful AI Tutor for software engineering and interview preparation.

User asks: {message}

Provide a clear, structured explanation with:
- Concept overview
- Code examples (use fenced code blocks with language specified)
- Real-world use cases
- Common interview questions on this topic

Format your response in clean Markdown."""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        traceback.print_exc()
        err_msg = str(e)
        if "429" in err_msg or "quota" in err_msg.lower():
            lower_msg = message.lower()
            topic = "Python" if "python" in lower_msg else ("SQL" if "sql" in lower_msg else ("JavaScript" if "javascript" in lower_msg else message))
            fallback_text = _get_fallback_notes(topic)
            return f"""⚠️ **AI Tutor Notice: API Quota Exceeded (429)**

The Gemini API rate limit has been exceeded. Please wait 1-2 minutes and try again. The quota will reset automatically.

Offline study guide details related to **{topic}**:

{fallback_text}"""
        return f"**Tutor Error:** {err_msg}"

NOTES_FALLBACK_BANK = {
    'python': """## Python Quick Reference\n\n### Core Concepts\n- **Variables** are dynamically typed\n- **Lists**: `[1, 2, 3]` — mutable, ordered\n- **Tuples**: `(1, 2, 3)` — immutable\n- **Dicts**: `{'key': 'value'}` — key-value store\n- **Sets**: `{1, 2, 3}` — unique values\n\n### Functions\n```python\ndef greet(name, greeting='Hello'):\n    return f\"{greeting}, {name}!\"\n```\n\n### OOP\n```python\nclass Animal:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        return f\"{self.name} speaks!\"\n```\n\n### Interview Q&A\n- **Mutable vs Immutable?** Lists/dicts are mutable; tuples/strings are immutable\n- **GIL?** Global Interpreter Lock — only one thread executes Python at a time\n- **list vs tuple?** Lists are mutable and slower; tuples are immutable and faster\n""",
    'sql': """## SQL Quick Reference\n\n### Core Commands\n```sql\nSELECT * FROM table WHERE condition;\nINSERT INTO table (col1) VALUES ('val');\nUPDATE table SET col = val WHERE id = 1;\nDELETE FROM table WHERE id = 1;\n```\n\n### Joins\n- **INNER JOIN** — rows matching in both tables\n- **LEFT JOIN** — all left rows + matching right\n- **RIGHT JOIN** — all right rows + matching left\n\n### Interview Q&A\n- **Primary Key?** Unique identifier for each row, cannot be NULL\n- **Foreign Key?** Links two tables together\n- **Index?** Speeds up SELECT queries\n""",
    'default': """## Study Notes: {topic}\n\n> ⚡ Quick Tip: We are displaying key concept notes related to your query.\n\n### Key Areas to Study\n1. **Core Concepts** — Basic definitions and theory\n2. **Practical Usage** — Real-world use cases and examples\n3. **Common Interview Questions** — Frequently asked questions\n4. **Best Practices** — Do's and Don'ts\n\n### Quick Checklist\n- [ ] Read official documentation\n- [ ] Practice with small projects\n- [ ] Solve 10 interview questions\n- [ ] Review and revise weekly\n\n*Note: If you encounter quota issues, please verify your query and try again.*"""
}

def _get_fallback_notes(topic):
    key = topic.strip().lower()
    for k, v in NOTES_FALLBACK_BANK.items():
        if k in key:
            return v
    return NOTES_FALLBACK_BANK['default'].format(topic=topic)

def api_notes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        topic = data.get('topic', '').strip()
        note_type = data.get('note_type', 'Detailed')
        if not topic:
            return JsonResponse({'error': 'Topic is required'}, status=400)
        result, err = generate_study_notes(topic, note_type)
        if err == 'quota_exceeded':
            fallback = _get_fallback_notes(topic)
            return JsonResponse({'notes': fallback, 'fallback': True})
        if err:
            return JsonResponse({'error': err}, status=500)
        return JsonResponse({'notes': result})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def generate_study_notes(topic, note_type):
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None, "API Key is missing. Please set GEMINI_API_KEY in your .env file."
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        format_instructions = {
            'Short Summary': 'a concise summary with key bullet points and a brief overview (max 300 words)',
            'Detailed Notes': 'comprehensive detailed notes with explanations, examples, and sub-sections',
            'Interview Q&A': '10 important interview questions with detailed answers for the topic',
            'Cheat Sheet': 'a cheat sheet with syntax, key commands, and quick reference points in a structured layout'
        }
        instruction = format_instructions.get(note_type, 'structured notes')

        prompt = f"""Generate {instruction} for the topic: **{topic}**

Requirements:
- Use clean Markdown formatting
- Include headings (##, ###) for sections
- Use bullet points and numbered lists where appropriate  
- Include code blocks with language specified (```python, ```js, etc.) for any code
- Make it interview-ready and practical"""

        response = model.generate_content(prompt, request_options={"timeout": 15.0})
        return response.text.strip(), None
    except Exception as e:
        traceback.print_exc()
        err = str(e)
        if '429' in err or 'quota' in err.lower() or 'rate' in err.lower() or 'deadline' in err.lower() or 'timeout' in err.lower():
            return None, "quota_exceeded"
        return None, f"Could not generate notes. Please try again later."

QUIZ_FALLBACK_BANK = {
    'python': [
        {
            "question": "Which of the following is mutable in Python?",
            "options": ["List", "Tuple", "String", "Integer"],
            "correct_index": 0,
            "explanation": "Lists can be modified after creation, making them mutable. Tuples, strings, and integers are immutable."
        },
        {
            "question": "How do you start a function definition in Python?",
            "options": ["func name()", "define name()", "def name()", "function name()"],
            "correct_index": 2,
            "explanation": "Python uses the 'def' keyword to declare a function."
        },
        {
            "question": "What does the 'len()' function do?",
            "options": ["Finds string character size", "Returns length of an iterable", "Returns memory size", "None of the above"],
            "correct_index": 1,
            "explanation": "The len() function returns the number of items in an iterable (like list, tuple, string, dictionary, etc.)."
        },
        {
            "question": "Which of these is not a core data type in Python?",
            "options": ["List", "Dictionary", "Class", "Tuple"],
            "correct_index": 2,
            "explanation": "Class is a user-defined blueprint, not a built-in core data type like lists, tuples, or dictionaries."
        },
        {
            "question": "How do you insert an comment in Python code?",
            "options": ["// comment", "/* comment */", "# comment", "<!-- comment -->"],
            "correct_index": 2,
            "explanation": "Python uses the hash character (#) to write single-line comments."
        }
    ],
    'sql': [
        {
            "question": "Which SQL statement is used to retrieve data?",
            "options": ["GET", "EXTRACT", "SELECT", "OPEN"],
            "correct_index": 2,
            "explanation": "The SELECT statement is used to query and fetch data from a database."
        },
        {
            "question": "What does a LEFT JOIN do?",
            "options": ["Returns all left table rows + matching right rows", "Returns matching rows only", "Returns all right rows", "None of the above"],
            "correct_index": 0,
            "explanation": "A LEFT JOIN returns all records from the left table, and matched records from the right table. Unmatched right rows return NULL."
        },
        {
            "question": "Which constraint uniquely identifies each row in a database table?",
            "options": ["FOREIGN KEY", "PRIMARY KEY", "UNIQUE", "NOT NULL"],
            "correct_index": 1,
            "explanation": "A PRIMARY KEY constraint uniquely identifies each record. It must contain unique values and cannot be NULL."
        },
        {
            "question": "How do you select all columns from a table named 'Users'?",
            "options": ["SELECT Users;", "SELECT * FROM Users;", "SELECT columns FROM Users;", "GET * FROM Users;"],
            "correct_index": 1,
            "explanation": "The asterisk (*) acts as a wildcard representing all columns in the table."
        },
        {
            "question": "Which command is used to add new rows to a table?",
            "options": ["ADD ROW", "INSERT INTO", "UPDATE", "APPEND"],
            "correct_index": 1,
            "explanation": "INSERT INTO is the standard SQL statement used to add new records to a database table."
        }
    ],
    'oops': [
        {
            "question": "Which OOP concept allows a subclass to inherit attributes and methods from a parent class?",
            "options": ["Polymorphism", "Encapsulation", "Inheritance", "Abstraction"],
            "correct_index": 2,
            "explanation": "Inheritance allows a new class (subclass) to inherit characteristics and behaviors from an existing class."
        },
        {
            "question": "What is Encapsulation?",
            "options": ["Hiding internal state and requiring all interaction through methods", "Creating multiple forms of a method", "Inheriting attributes from a parent class", "Defining a class blueprint"],
            "correct_index": 0,
            "explanation": "Encapsulation wraps data (variables) and code (methods) together as a single unit and restricts direct access."
        },
        {
            "question": "What is Polymorphism?",
            "options": ["Restricting class access", "Hiding implementation details", "Ability of different classes to respond to the same method call differently", "Reusing code"],
            "correct_index": 2,
            "explanation": "Polymorphism means 'many forms' and allows objects of different classes to be treated as objects of a common superclass."
        },
        {
            "question": "Which of these is used to define blueprint specifications without implementation?",
            "options": ["Abstract Class/Interface", "Subclass", "Concrete Class", "Static Method"],
            "correct_index": 0,
            "explanation": "Interfaces and abstract classes define structures/methods that subclasses must implement."
        },
        {
            "question": "What is an Instance of a class called?",
            "options": ["Method", "Variable", "Object", "Constructor"],
            "correct_index": 2,
            "explanation": "An object is a concrete instance of a class."
        }
    ],
    'default': [
        {
            "question": "What is the main advantage of Version Control Systems (e.g. Git)?",
            "options": ["Speeds up computers", "Tracks history and coordinates team work", "Compiles code faster", "Secures local files"],
            "correct_index": 1,
            "explanation": "Version control systems track file history and allow multiple developers to collaborate without overwriting work."
        },
        {
            "question": "Which data structure operates on a Last-In, First-Out (LIFO) basis?",
            "options": ["Queue", "List", "Stack", "Tree"],
            "correct_index": 2,
            "explanation": "A stack pushes items and pops them from the same end, meaning the last item added is the first one removed."
        },
        {
            "question": "What is the primary role of an API?",
            "options": ["Build user interfaces", "Connect databases", "Enable different software programs to communicate", "Compile source code"],
            "correct_index": 2,
            "explanation": "Application Programming Interfaces (APIs) define protocols and tools allowing different applications to exchange data."
        },
        {
            "question": "What does HTML stand for?",
            "options": ["Hyper Text Markup Language", "High Tech Multi Language", "Hyperlink Text Management List", "Home Tool Markup Language"],
            "correct_index": 0,
            "explanation": "HTML is the standard markup language used to structure pages on the World Wide Web."
        },
        {
            "question": "Which of the following is a key advantage of cloud computing?",
            "options": ["Requires no internet", "Higher physical hardware cost", "On-demand scalability and resource sharing", "Runs only offline"],
            "correct_index": 2,
            "explanation": "Cloud computing offers flexible resources, scaling on-demand without managing physical servers directly."
        }
    ]
}

def _get_fallback_quiz(topic):
    key = topic.strip().lower()
    for k, v in QUIZ_FALLBACK_BANK.items():
        if k in key:
            return v
    return QUIZ_FALLBACK_BANK['default']

def generate_quiz(topic):
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return _get_fallback_quiz(topic)
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""You are a quiz generation assistant.
        Analyze the quiz topic requested: "{topic}".
        
        If the topic is random gibberish, offensive words, spam, or completely meaningless text (for example, "asdasd", "qwerty", "hgdskjhdfs"), you MUST return ONLY a JSON object containing an error key with an error message:
        {{"error": "Please enter a valid study or technical topic."}}
        
        Otherwise, generate a 5-question multiple choice quiz about "{topic}".
        Return ONLY a JSON array of objects. Each object must have:
        "question" (string),
        "options" (list of 4 strings),
        "correct_index" (integer 0-3),
        "explanation" (string).
        """
        response = model.generate_content(prompt)
        import re
        text = response.text.strip()
        
        # Check if an error object was returned
        if '"error":' in text or 'error' in text.lower():
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                parsed_err = json.loads(match.group(0))
                if 'error' in parsed_err:
                    return parsed_err
                    
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if match: text = match.group(0)
        parsed = json.loads(text)
        if parsed and len(parsed) > 0:
            return parsed
        return _get_fallback_quiz(topic)
    except Exception as e:
        traceback.print_exc()
        return _get_fallback_quiz(topic)

def generate_career_analysis(skills, performance):
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return {"level": "Junior", "strong": ["N/A"], "weak": ["N/A"], "actions": ["Practice more"]}
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""Analyze career trajectory based on skills: {skills} and interview avg score: {performance}%.
        Return ONLY JSON object with:
        "level" (string, e.g., "Junior Developer", "Mid-Level Engineer"),
        "strong" (list of 3 strings),
        "weak" (list of 2 strings),
        "actions" (list of 3 recommended actions).
        """
        response = model.generate_content(prompt)
        import re
        text = response.text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match: text = match.group(0)
        return json.loads(text)
    except:
        return {"level": "Unknown", "strong": [], "weak": [], "actions": []}

ROADMAP_FALLBACK_BANK = {
    'python': {
        "day30": [
            "Master Python fundamentals (OOP, decorators, generators)",
            "Practice basic data structures (lists, dicts, stacks, queues)",
            "Learn Python testing frameworks (unittest, pytest)"
        ],
        "day60": [
            "Learn Django or Flask web framework and build a REST API",
            "Understand database integration (SQLAlchemy, PostgreSQL)",
            "Build 1-2 dynamic backend web application projects"
        ],
        "day90": [
            "Practice 30+ medium-level coding interview problems",
            "Prepare system design basics (REST, caching, rate limiting)",
            "Optimize resume and GitHub profile for Python roles"
        ]
    },
    'java': {
        "day30": [
            "Master Java Core concepts (OOP, Collections, Multithreading, Exceptions)",
            "Learn Maven or Gradle build tools and Java project structures",
            "Practice writing clean Java code and basic JUnit unit testing"
        ],
        "day60": [
            "Learn Spring Framework and Spring Boot to build RESTful APIs",
            "Understand JPA/Hibernate ORM and database integrations (MySQL/PostgreSQL)",
            "Build 1-2 Enterprise Backend applications using Spring Boot"
        ],
        "day90": [
            "Solve 30+ medium coding challenges on LeetCode using Java",
            "Study microservices architecture and cloud deployment basics",
            "Optimize resume and GitHub showcasing Java/Spring Boot expertise"
        ]
    },
    'javascript': {
        "day30": [
            "Master modern JavaScript (ES6+, Promises, Async/Await, DOM manipulation)",
            "Learn package managers (NPM/Yarn) and dev tooling setups",
            "Build 2-3 interactive dynamic vanilla JS frontend projects"
        ],
        "day60": [
            "Learn React.js (Hooks, state management, router) or Vue/Angular",
            "Understand API integration, JSON communication, and web security",
            "Build a responsive single page application (SPA) portfolio website"
        ],
        "day90": [
            "Practice 25+ algorithmic coding problems in JavaScript",
            "Learn basic Node.js/Express for full-stack integration capability",
            "Polish resume showcasing JS/React modern web development skills"
        ]
    },
    'sql': {
        "day30": [
            "Master complex SELECT queries, subqueries, and aggregation",
            "Understand all JOIN types (INNER, LEFT, RIGHT, FULL)",
            "Learn database design principles and normalization (1NF, 2NF, 3NF)"
        ],
        "day60": [
            "Write optimized stored procedures, triggers, and views",
            "Understand indexes (Clustered, Non-clustered) and query plans",
            "Build an analytics dashboard connecting to a SQL database"
        ],
        "day90": [
            "Practice 20+ query optimization problems on LeetCode",
            "Prepare database scaling concepts (sharding, replication)",
            "Review transaction isolation levels and ACID properties"
        ]
    },
    'default': {
        "day30": [
            "Audit your current skills and define target role requirements",
            "Establish a daily coding and theoretical study routine",
            "Review computer science fundamentals (data structures, algorithms)"
        ],
        "day60": [
            "Build 1 core portfolio project showing your selected skill path",
            "Learn git collaboration and deploy project to a cloud platform",
            "Begin solving topic-specific mock assessment questions daily"
        ],
        "day90": [
            "Take 5+ mock interviews to test communication and tech skills",
            "Polish your professional portfolio website and LinkedIn headline",
            "Apply systematically to 5-10 target positions weekly"
        ]
    }
}

def _get_fallback_roadmap(goal, skills):
    goal_clean = goal.strip().lower()
    skills_clean = skills.strip().lower()
    
    # 1. Prioritize matching the goal
    for k, v in ROADMAP_FALLBACK_BANK.items():
        if k != 'default' and k in goal_clean:
            return v
            
    # 2. Secondary check for skills
    for k, v in ROADMAP_FALLBACK_BANK.items():
        if k != 'default' and k in skills_clean:
            return v
            
    return ROADMAP_FALLBACK_BANK['default']

def generate_roadmap(goal, skills):
    # Goal validation check
    valid_keywords = [
        'developer', 'engineer', 'manager', 'analyst', 'designer', 'consultant', 'scientist', 'architect',
        'programmer', 'tester', 'lead', 'director', 'specialist', 'admin', 'administrator', 'expert',
        'python', 'java', 'javascript', 'html', 'css', 'sql', 'c#', 'c++', 'ruby', 'php', 'swift', 'kotlin',
        'rust', 'go', 'typescript', 'react', 'node', 'angular', 'vue', 'django', 'flask', 'spring', 'aws',
        'cloud', 'database', 'system', 'network', 'security', 'devops', 'machine learning', 'ai', 'data',
        'web', 'frontend', 'backend', 'full stack', 'fullstack', 'qa', 'testing', 'embedded', 'mobile',
        'ios', 'android', 'salesforce', 'ui', 'ux', 'product', 'project', 'sap', 'scrum', 'agile'
    ]
    
    goal_words = re.findall(r'\w+', goal.lower())
    is_valid = False
    for word in goal_words:
        if any(kw in word or word in kw for kw in valid_keywords if len(word) >= 3):
            is_valid = True
            break
            
    if not is_valid:
        return {"error": "Please enter a valid career goal, job role, or technology skill path (e.g. Java, Python, Web Developer)."}

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return _get_fallback_roadmap(goal, skills)
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""You are a professional career advisor.
        First, check if '{goal}' is a valid professional career goal, job role, or technology skill path.
        If it is NOT a valid career path (e.g., if it is random text, spam, nonsense, gibberish like 'antigravity', or completely unrelated to professional jobs/skills), return ONLY a JSON object with an "error" key explaining that it is invalid, like:
        {{"error": "Please enter a valid career goal or job role."}}

        If it IS a valid career path, generate a structured 90-day roadmap to achieve '{goal}' given current skills: {skills}.
        Return ONLY a JSON object with 3 keys: "day30", "day60", "day90".
        Each key must contain a list of 3-4 string milestones.
        """
        response = model.generate_content(prompt)
        text = response.text.strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match: text = match.group(0)
        parsed = json.loads(text)
        if "error" in parsed or ("day30" in parsed and "day60" in parsed and "day90" in parsed):
            return parsed
        return _get_fallback_roadmap(goal, skills)
    except Exception as e:
        traceback.print_exc()
        return _get_fallback_roadmap(goal, skills)

def improve_resume_text(text):
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "Developed and deployed a highly responsive e-commerce web application utilizing Python and Django, resulting in a 30% increase in user engagement."
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        Rewrite the following bullet point or summary from a resume to be highly professional, action-oriented, and impactful.
        Original: {text}
        
        Return ONLY the rewritten version. Do not include quotes, greetings, or other text.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error improving resume text: {e}")
        return "Developed and deployed a highly responsive e-commerce web application utilizing Python and Django."

def generate_cover_letter(resume_text, job_title, company_name, job_desc):
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return f"Dear Hiring Team at {company_name or 'the Company'},\n\nI am writing to express my strong interest in the {job_title or 'Software Engineer'} position. With my background, I am confident in my ability to contribute effectively to your team.\n\nThank you for your time and consideration.\n\nSincerely,\n[Your Name]"

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""You are a professional career writer. Write a tailored, persuasive cover letter for:
        Job Title: {job_title}
        Company Name: {company_name}
        Job Description: {job_desc}
        
        Use the candidate's resume/profile details to highlight relevant achievements:
        Candidate Profile: {resume_text}
        
        The cover letter should be highly professional, engaging, and match the job requirements. Keep it under 400 words. Return ONLY the cover letter text. Do not add markdown backticks wrapper, just return raw paragraphs.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        traceback.print_exc()
        return f"Dear Hiring Team at {company_name or 'the Company'},\n\nI am writing to express my strong interest in the {job_title or 'Software Engineer'} position. With my background, I am confident in my ability to contribute effectively to your team.\n\nThank you for your time and consideration.\n\nSincerely,\n[Your Name]"

