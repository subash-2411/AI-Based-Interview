from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import UserHistory, DailyQuizLimit, Skill
from .forms import StudentRegisterForm, StudentLoginForm, ProfileUpdateForm
from django.contrib import messages
from django.http import JsonResponse
import json
import os
import re
from datetime import date
def register_view(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')  <-- Auto-login removed
            messages.success(request, f"Account created for {user.username}! Please login to continue.")
            return redirect('login')
    else:
        form = StudentRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = StudentLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = StudentLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        from .models import Skill

        # Handle Delete Skill
        delete_skill_id = request.POST.get('delete_skill_id')
        if delete_skill_id:
            try:
                skill = Skill.objects.get(id=delete_skill_id, user=request.user)
                skill_name = skill.name
                skill.delete()
                messages.success(request, f"Removed skill: {skill_name}")
            except Skill.DoesNotExist:
                pass
            return redirect('profile')

        # Handle Add Skill
        new_skill = request.POST.get('new_skill', '').strip()
        if new_skill:
            if len(new_skill) > 30:
                messages.error(request, "Skill name is too long.")
            else:
                if not Skill.objects.filter(user=request.user, name__iexact=new_skill).exists():
                    Skill.objects.create(user=request.user, name=new_skill)
                    messages.success(request, f"Added skill: {new_skill}")
                else:
                    messages.info(request, f"You already have {new_skill} in your profile.")
        return redirect('profile')

    history, created = UserHistory.objects.get_or_create(user=request.user)
    skills = request.user.skills.all()
    
    context = {
        'history': history,
        'skills': skills,
        'user': request.user
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)
    
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'title': 'Edit Profile'
    })

@login_required
def generate_quick_quiz(request):
    skill_name = request.GET.get('skill', '').strip()
    if not skill_name:
        return JsonResponse({'error': 'Skill name is required'}, status=400)
        
    today = date.today()
    limit_obj, created = DailyQuizLimit.objects.get_or_create(user=request.user, skill_name=skill_name, date=today)
    
    if limit_obj.attempts >= 3:
        return JsonResponse({'status': 'limit_reached', 'message': f"You have reached the limit of 3 {skill_name} quizzes for today! Check back tomorrow."})
        
    # Get history of asked questions from session to avoid repeats
    asked_history = request.session.get('asked_quiz_questions', {})
    skill_history = asked_history.get(skill_name.lower(), [])
    
    try:
        import google.generativeai as genai
        import random
        raw_api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""
        valid_keys = [k.strip() for k in raw_api_key.split(',') if k.strip()]
        if not valid_keys:
            raise ValueError("No valid API key")
            
        genai.configure(api_key=valid_keys[0])
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        history_context = ""
        if skill_history:
            recent_qs = "\n- ".join(skill_history[-15:])
            history_context = f"\nCRITICAL: Do NOT repeat any of these previously asked questions or exact concepts:\n- {recent_qs}\n"

        prompt = f"""
        Generate a unique, high-quality multiple choice technical interview question specifically for the skill/technology: {skill_name}.
        Difficulty: Medium.
        Target domain concepts: syntax, data structures, algorithms, runtime behavior, standard libraries, or architectural best practices in {skill_name}.
        {history_context}
        
        Return ONLY a JSON object with this exact structure:
        {{
            "question": "What is ...?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_index": 0,
            "explanation": "Brief explanation of why the correct option is right."
        }}
        """
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json", "temperature": 0.8}
        )
        quiz_data = json.loads(response.text)
        
        # Save to session to ensure no repeats
        if 'question' in quiz_data:
            if 'asked_quiz_questions' not in request.session:
                request.session['asked_quiz_questions'] = {}
            if skill_name.lower() not in request.session['asked_quiz_questions']:
                request.session['asked_quiz_questions'][skill_name.lower()] = []
            request.session['asked_quiz_questions'][skill_name.lower()].append(quiz_data['question'])
            request.session.modified = True
            
        return JsonResponse({'status': 'success', 'quiz': quiz_data})
        
    except Exception as e:
        print(f"Quiz Error: {e}")
        import random
        # Skill specific fallbacks with variety
        fallbacks_by_skill = {
            "python": [
                {
                    "question": "Which of the following data types in Python is immutable?",
                    "options": ["List", "Dictionary", "Tuple", "Set"],
                    "correct_index": 2,
                    "explanation": "Tuples in Python cannot be modified once created, making them immutable."
                },
                {
                    "question": "What does the Python `__init__` method represent?",
                    "options": ["A class destructor", "A constructor method", "A static method", "An import hook"],
                    "correct_index": 1,
                    "explanation": "`__init__` acts as a constructor in Python to initialize newly created object instances."
                },
                {
                    "question": "How do you create a generator function in Python?",
                    "options": ["By using the `yield` keyword", "By using the `return` keyword", "By inheriting from `Generator`", "By using `async def` only"],
                    "correct_index": 0,
                    "explanation": "A generator function contains at least one `yield` statement."
                },
                {
                    "question": "What is the output of `type(lambda x: x)` in Python?",
                    "options": ["<class 'function'>", "<class 'lambda'>", "<class 'object'>", "<class 'method'>"],
                    "correct_index": 0,
                    "explanation": "In Python, lambda expressions produce standard first-class function objects."
                }
            ],
            "sql": [
                {
                    "question": "Which SQL clause is used to filter group results after a GROUP BY?",
                    "options": ["WHERE", "HAVING", "ORDER BY", "FILTER"],
                    "correct_index": 1,
                    "explanation": "`HAVING` filters aggregate/group data, whereas `WHERE` filters individual rows before grouping."
                },
                {
                    "question": "What is the difference between `UNION` and `UNION ALL` in SQL?",
                    "options": ["UNION removes duplicates, UNION ALL retains all rows", "UNION is faster", "UNION ALL removes duplicates", "There is no difference"],
                    "correct_index": 0,
                    "explanation": "UNION runs a distinct sort to eliminate duplicate rows, while UNION ALL returns all rows."
                },
                {
                    "question": "Which SQL constraint uniquely identifies each record in a database table?",
                    "options": ["FOREIGN KEY", "PRIMARY KEY", "CHECK", "UNIQUE NOT NULL"],
                    "correct_index": 1,
                    "explanation": "A PRIMARY KEY constraint uniquely identifies each row and cannot contain NULL values."
                }
            ],
            "javascript": [
                {
                    "question": "What will `typeof NaN` evaluate to in JavaScript?",
                    "options": ["'undefined'", "'null'", "'number'", "'NaN'"],
                    "correct_index": 2,
                    "explanation": "In JavaScript, NaN (Not-a-Number) is formally of type 'number'."
                },
                {
                    "question": "Which method removes the last element from an array in JavaScript?",
                    "options": ["shift()", "pop()", "slice()", "splice()"],
                    "correct_index": 1,
                    "explanation": "`pop()` removes the last element of an array and returns it."
                }
            ]
        }
        
        skill_key = skill_name.lower()
        candidates = fallbacks_by_skill.get(skill_key, [
            {
                "question": f"What is a fundamental building block of {skill_name}?",
                "options": ["Modularity & Functions", "Memory Isolation", "Compilation optimization", "All of the above"],
                "correct_index": 0,
                "explanation": f"Modularity is a core concept across {skill_name} development."
            },
            {
                "question": f"Which design pattern is commonly used when structuring code in {skill_name}?",
                "options": ["Singleton", "Factory", "Observer", "All of the above"],
                "correct_index": 3,
                "explanation": "Most modern programming ecosystems utilize creational, structural, and behavioral patterns."
            }
        ])
        
        # Pick one not yet in session history if possible
        unseen = [c for c in candidates if c["question"] not in skill_history]
        chosen = random.choice(unseen) if unseen else random.choice(candidates)
        
        if 'asked_quiz_questions' not in request.session:
            request.session['asked_quiz_questions'] = {}
        if skill_name.lower() not in request.session['asked_quiz_questions']:
            request.session['asked_quiz_questions'][skill_name.lower()] = []
        request.session['asked_quiz_questions'][skill_name.lower()].append(chosen['question'])
        request.session.modified = True
        
        return JsonResponse({'status': 'success', 'quiz': chosen})

@login_required
def submit_quick_quiz(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            skill_name = data.get('skill', '')
            is_correct = data.get('is_correct', False)
            
            today = date.today()
            limit_obj, created = DailyQuizLimit.objects.get_or_create(user=request.user, skill_name=skill_name, date=today)
            
            if limit_obj.attempts < 3:
                limit_obj.attempts += 1
                if is_correct:
                    limit_obj.score += 1
                    
                    history, _ = UserHistory.objects.get_or_create(user=request.user)
                    history.xp += 10
                    history.save()
                    
                limit_obj.save()
                
            return JsonResponse({
                'status': 'success', 
                'attempts_left': 3 - limit_obj.attempts,
                'score_today': limit_obj.score,
                'is_correct': is_correct
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
