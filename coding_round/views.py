from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CodingProblem, CodingSubmission
from django.http import JsonResponse
import json

@login_required
def coding_list_view(request):
    user_skills = request.user.skills.all()
    skill_names = [s.name.lower() for s in user_skills]
    
    user_problems = CodingProblem.objects.filter(user=request.user).order_by('-id')
    global_problems = CodingProblem.objects.filter(user__isnull=True)
    
    # Create some dummy problems with tags if none exist
    if not global_problems.exists() and not user_problems.exists():
        CodingProblem.objects.create(
            title="Two Sum",
            description="Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
            difficulty="Easy",
            tags="Python, Array, Logic"
        )
        CodingProblem.objects.create(
            title="Reverse Linked List",
            description="Given the head of a singly linked list, reverse the list, and return the reversed list.",
            difficulty="Medium",
            tags="Python, Linked List, Recursion"
        )
        CodingProblem.objects.create(
            title="Database Query Optimization",
            description="Optimize a complex SQL query for high performance.",
            difficulty="Hard",
            tags="SQL, Database, Backend"
        )
        global_problems = CodingProblem.objects.filter(user__isnull=True)

    # Combine problems: personalized first, then global
    problems = list(user_problems) + list(global_problems)

    # Process problems for the template
    for problem in problems:
        problem_tags = [t.strip().lower() for t in problem.tags.split(',')]
        if problem.user == request.user:
            problem.is_recommended = True
        else:
            problem.is_recommended = any(skill in skill_names for skill in problem_tags)
        problem.tag_list = [t.strip() for t in problem.tags.split(',')]
        
    context = {
        'problems': problems,
        'user_skills': user_skills,
        'has_coding_profile': user_problems.exists()
    }
    return render(request, 'coding_round/list.html', context)

@login_required
def coding_editor_view(request, problem_id):
    problem = get_object_or_404(CodingProblem, id=problem_id)
    return render(request, 'coding_round/editor.html', {'problem': problem})

@login_required
def submit_code_api(request, problem_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code')
        
        problem = get_object_or_404(CodingProblem, id=problem_id)
        
        # Simulating code execution and scoring
        # In a real app, you might use a sandboxed execution environment
        score = 0
        if "def solution" in code:
            score = 100
        else:
            score = 50
            
        submission = CodingSubmission.objects.create(
            user=request.user,
            problem=problem,
            user_code=code,
            score=score
        )
        
        return JsonResponse({'status': 'success', 'score': score, 'submission_id': submission.id})
        
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def coding_setup_view(request):
    return render(request, 'coding_round/setup.html')

@login_required
def generate_practice_api(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        from resume.models import Resume
        from resume.utils import extract_text_from_pdf, extract_text_from_docx
        from ai_engine.logic import generate_coding_problems
        import os
        
        file = request.FILES['resume']
        resume_obj = Resume.objects.create(user=request.user, file=file)
        file_path = resume_obj.file.path
        ext = os.path.splitext(file_path)[1].lower()
        text = ""
        if ext == '.pdf': text = extract_text_from_pdf(file_path)
        elif ext == '.docx': text = extract_text_from_docx(file_path)
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                
        resume_obj.extracted_text = text
        resume_obj.save()
        
        # Generate personalized problems
        problems_json = generate_coding_problems(text, count=3)
        
        if isinstance(problems_json, dict):
            if 'problems' in problems_json:
                problems_json = problems_json['problems']
            elif 'coding_problems' in problems_json:
                problems_json = problems_json['coding_problems']
            else:
                # Try to find any list in the dict values
                for v in problems_json.values():
                    if isinstance(v, list):
                        problems_json = v
                        break
        
        if problems_json and isinstance(problems_json, list):
            for p in problems_json:
                if not isinstance(p, dict):
                    continue
                CodingProblem.objects.create(
                    user=request.user,
                    title=str(p.get('title', 'Coding Challenge'))[:200],
                    description=str(p.get('description', '')),
                    difficulty=str(p.get('difficulty', 'Medium'))[:20],
                    tags=str(p.get('tags', ''))[:200],
                    language=str(p.get('language', 'Python'))[:50],
                    initial_code=str(p.get('initial_code', 'def solution():\n    pass'))
                )
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'AI failed to generate problems.'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'No resume provided.'}, status=400)

@login_required
def get_hint_api(request, problem_id):
    if request.method == 'POST':
        from ai_engine.logic import get_coding_hint
        data = json.loads(request.body)
        user_code = data.get('code', '')
        hint_lang = data.get('language', 'ta-EN')
        
        problem = get_object_or_404(CodingProblem, id=problem_id)
        hint = get_coding_hint(problem.title, problem.description, user_code, language=hint_lang)
        
        return JsonResponse({'status': 'success', 'hint': hint})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def generate_single_challenge_api(request):
    if request.method == 'POST':
        import json
        from resume.models import Resume
        from ai_engine.logic import get_fallback_coding_problems
        import google.generativeai as genai
        import os
        
        data = json.loads(request.body)
        lang = data.get('language', 'Python').strip()
        
        # Get user resume
        resumes = Resume.objects.filter(user=request.user)
        resume_text = ""
        if resumes.exists():
            resume_text = resumes.latest('uploaded_at').extracted_text
            
        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        
        # We will generate a problem in the selected language
        new_problem = None
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                resume_context = f"The candidate's resume content is:\n{resume_text[:2000]}" if resume_text else "No resume available."
                
                prompt = f"""
                You are an expert technical interviewer.
                Generate exactly ONE coding problem to test the candidate in the programming language: {lang}.
                {resume_context}
                
                Return ONLY a JSON object with the following fields:
                - "title": A short title for the problem (e.g., "Two Sum" or "Array Reversal").
                - "description": A clear description of the problem, input/output requirements, and an example.
                - "difficulty": "Easy", "Medium", or "Hard".
                - "tags": Comma-separated tags (e.g., "{lang}, Arrays, Algorithms").
                - "initial_code": Starter code boilerplate in {lang} that the user will complete (e.g. `def solution(nums, target):` or `function solution(nums, target) {{}}`).
                
                Ensure the JSON format is perfectly valid. Return ONLY the raw JSON text. Do not use ```json formatting.
                """
                response = model.generate_content(prompt, request_options={"timeout": 15.0})
                text = response.text.strip()
                
                import re
                match = re.search(r'\{.*\}', text, re.DOTALL)
                if match:
                    p = json.loads(match.group(0))
                    new_problem = CodingProblem.objects.create(
                        user=request.user,
                        title=str(p.get('title', 'Coding Challenge'))[:200],
                        description=str(p.get('description', '')),
                        difficulty=str(p.get('difficulty', 'Medium'))[:20],
                        tags=str(p.get('tags', ''))[:200],
                        language=lang,
                        initial_code=str(p.get('initial_code', ''))
                    )
            except Exception as e:
                print(f"Error generating single coding challenge: {e}")
                
        if not new_problem:
            # Fallback
            fallbacks = get_fallback_coding_problems([], count=1)
            f = fallbacks[0]
            initial_code = f.get('initial_code')
            if lang.lower() == 'javascript':
                initial_code = "function solution(n) {\n    // Write code here\n}"
            elif lang.lower() == 'java':
                initial_code = "public class Solution {\n    public static void main(String[] args) {\n        // Write code here\n    }\n}"
            elif lang.lower() == 'c++':
                initial_code = "#include <iostream>\nusing namespace std;\n\nvoid solution() {\n    // Write code here\n}"
                
            new_problem = CodingProblem.objects.create(
                user=request.user,
                title=f.get('title'),
                description=f.get('description'),
                difficulty=f.get('difficulty'),
                tags=f.get('tags'),
                language=lang,
                initial_code=initial_code
            )
            
        return JsonResponse({'status': 'success', 'problem_id': new_problem.id})
        
    return JsonResponse({'status': 'error'}, status=400)
