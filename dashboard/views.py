from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import UserHistory, ThemePreference
from interview.models import InterviewSession
from resume.models import Resume
from resume.utils import extract_text_from_pdf, extract_text_from_docx, extract_skills, calculate_ats_score
import json
import os
import re


def home_view(request):
    return render(request, 'dashboard/home.html')

@login_required
def dashboard_view(request):
    # Temp migration runner inside view
    from django.core.management import call_command
    try:
        call_command('makemigrations', 'interview', interactive=False)
        call_command('migrate', interactive=False)
    except Exception as e:
        print(f"Migration error: {e}")
        
    history, created = UserHistory.objects.get_or_create(user=request.user)
    recent_sessions = InterviewSession.objects.filter(user=request.user, is_completed=True).order_by('-created_at')[:5]
    recent_sessions_data = []
    for s in recent_sessions:
        resume_name = "General Interview"
        if s.resume and s.resume.file:
            base_name = os.path.basename(s.resume.file.name)
            resume_name = re.sub(r'_[a-zA-Z0-9]{7,10}(\.[a-zA-Z0-9]+)$', r'\1', base_name)
        recent_sessions_data.append({
            'id': s.id,
            'category': f"Technical Interview ({s.difficulty})",
            'created_at': s.created_at,
            'score': s.score,
            'resume_name': resume_name
        })
    
    # Get scores for the performance chart
    chart_sessions = InterviewSession.objects.filter(user=request.user, is_completed=True).order_by('created_at')[:6]
    chart_data = [s.score for s in chart_sessions]
    chart_labels = [s.created_at.strftime('%b %d') for s in chart_sessions]
    
    # Calculate Gauge Offset (Circumference is 377)
    # Score 0% -> offset 377, Score 100% -> offset 0
    avg_score = history.avg_score or 0
    readiness_offset = 377 - (377 * (avg_score / 100))
    
    skills = request.user.skills.all()
    total_resumes = Resume.objects.filter(user=request.user).count()
    
    latest_resume = Resume.objects.filter(user=request.user).order_by('-uploaded_at').first()
    clean_filename = ""
    if latest_resume and latest_resume.file:
        base_name = os.path.basename(latest_resume.file.name)
        clean_filename = re.sub(r'_[a-zA-Z0-9]{7,10}(\.[a-zA-Z0-9]+)$', r'\1', base_name)
    
    context = {
        'history': history,
        'user': request.user,
        'recent_sessions': recent_sessions_data,
        'skills': skills,
        'chart_data_json': json.dumps(chart_data),
        'chart_labels_json': json.dumps(chart_labels),
        'readiness_offset': readiness_offset,
        'total_resumes': total_resumes,
        'latest_resume': latest_resume,
        'clean_filename': clean_filename
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def learning_view(request):
    history, created = UserHistory.objects.get_or_create(user=request.user)
    skills = request.user.skills.all()
    
    linkedin_tips = [
        {'icon': 'fas fa-user-circle', 'title': 'Professional Photo', 'desc': 'Profiles with a professional headshot get 21x more views and 36x more messages from recruiters.'},
        {'icon': 'fas fa-heading', 'title': 'Keyword-Rich Headline', 'desc': 'Use your target job title + top 2-3 skills (e.g., "Python Developer | Django | REST APIs") for maximum ATS visibility.'},
        {'icon': 'fas fa-align-left', 'title': 'Compelling About Section', 'desc': 'Write 3-5 sentences on who you are, what you do best, and what you are looking for. Use first person.'},
        {'icon': 'fas fa-trophy', 'title': 'Quantify Achievements', 'desc': 'Replace duties with results: "Reduced API response time by 40%" beats "Worked on backend APIs" every time.'},
        {'icon': 'fas fa-certificate', 'title': 'Add Certifications', 'desc': 'Cloud, AI, or framework certifications from Google, AWS, or Coursera dramatically increase recruiter reach-outs.'},
        {'icon': 'fas fa-users', 'title': 'Grow Your Network', 'desc': 'Connecting with 50+ people in your industry significantly boosts your profile\'s algorithm ranking on LinkedIn.'},
    ]
    roadmap_phases = [
        {'num': '1', 'label': 'Month 1-2', 'title': 'Foundation & Skills Audit', 'desc': 'Analyze your resume gaps, complete the AI interview simulation, and identify 2-3 key skills to strengthen.', 'color': '#8b5cf6', 'color_bg': 'rgba(139,92,246,0.1)'},
        {'num': '2', 'label': 'Month 2-3', 'title': 'Technical Skill Building', 'desc': 'Complete DSA fundamentals, build 1-2 portfolio projects, and get coding round certified in your primary language.', 'color': '#06b6d4', 'color_bg': 'rgba(6,182,212,0.1)'},
        {'num': '3', 'label': 'Month 3-4', 'title': 'Interview Preparation', 'desc': 'Run 10+ AI mock interviews, practice behavioral responses using STAR method, and optimize your LinkedIn profile.', 'color': '#10b981', 'color_bg': 'rgba(16,185,129,0.1)'},
        {'num': '4', 'label': 'Month 4-5', 'title': 'Active Job Search', 'desc': 'Apply to 5-10 targeted roles per week, reach out to recruiters, and leverage your network for referrals.', 'color': '#f59e0b', 'color_bg': 'rgba(245,158,11,0.1)'},
        {'num': '5', 'label': 'Month 5-6', 'title': 'Offer & Negotiation', 'desc': 'Evaluate offers using salary benchmarks, negotiate confidently, and close your target role!', 'color': '#ec4899', 'color_bg': 'rgba(236,72,153,0.1)'},
    ]
    return render(request, 'dashboard/learning.html', {
        'linkedin_tips': linkedin_tips,
        'roadmap_phases': roadmap_phases,
        'history': history,
        'skills': skills,
    })

@login_required
def jobs_view(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
    latest_resume = resumes.first()
    skills_list = request.user.skills.all()
    skills_str = ", ".join([s.name for s in skills_list]) if skills_list.exists() else "Python, Django, SQL"
    resume_text = latest_resume.extracted_text if latest_resume else ""
    return render(request, 'dashboard/jobs.html', {
        'resumes': resumes,
        'resume_text': resume_text,
        'skills_str': skills_str,
    })

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_dashboard_view(request):
    sessions = InterviewSession.objects.filter(is_completed=True).order_by('-created_at')
    context = {
        'sessions': sessions
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

# --- AI Feature API Endpoints ---
from django.http import JsonResponse
from ai_engine.new_features import *
import json

@login_required
def api_job_match(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        resume_text = data.get('resume_text', '')
        job_desc = data.get('job_desc', '')
        result = generate_job_match(resume_text, job_desc)
        return JsonResponse(result)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def api_salary_predict(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = predict_salary(data.get('skills', ''), data.get('experience', ''), data.get('location', ''))
        return JsonResponse({'salary': result})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def api_company_prep(request):
    company = request.GET.get('company', '')
    result = generate_company_prep_guide(company)
    return JsonResponse(result)

@login_required
def api_tutor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        result = chat_with_ai_tutor(message)
        return JsonResponse({'reply': result})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def api_notes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        topic = data.get('topic', '').strip()
        note_type = data.get('note_type', 'Detailed')
        if not topic:
            return JsonResponse({'error': 'Topic is required'}, status=400)
        from ai_engine.new_features import _get_fallback_notes
        result, err = generate_study_notes(topic, note_type)
        if err:
            # Fallback to local preset notes on any error/timeout
            return JsonResponse({'notes': _get_fallback_notes(topic), 'fallback': True})
        return JsonResponse({'notes': result})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def api_quiz(request):
    topic = request.GET.get('topic', '')
    result = generate_quiz(topic)
    if isinstance(result, dict) and 'error' in result:
        return JsonResponse({'error': result['error']}, status=400)
    return JsonResponse({'quiz': result})

@login_required
def api_career_coach(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = generate_career_analysis(data.get('skills', ''), data.get('performance', ''))
        return JsonResponse(result)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def api_career_coach_upload(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        file = request.FILES['resume']
        resume_obj = Resume.objects.create(user=request.user, file=file)
        file_path = resume_obj.file.path
        ext = os.path.splitext(file_path)[1].lower()
        text = ""
        try:
            if ext == '.pdf':
                text = extract_text_from_pdf(file_path)
            elif ext == '.docx':
                text = extract_text_from_docx(file_path)
            else:
                text = file.read().decode('utf-8', errors='ignore')
        except Exception as e:
            resume_obj.delete()
            return JsonResponse({'status': 'error', 'message': f'Failed to read file: {str(e)}'}, status=400)
            
        lower_text = text.lower()
        has_email = re.search(r'[\w\.-]+@[\w\.-]+', text)
        has_phone = re.search(r'(\d{10})', text)
        resume_keywords = ['experience', 'work', 'education', 'skills', 'projects', 'summary', 'profile', 'history', 'university', 'college', 'school', 'developer', 'engineer', 'analyst', 'manager']
        keyword_count = sum(1 for keyword in resume_keywords if keyword in lower_text)
        found_skills = extract_skills(text)
        
        if len(text.strip()) < 150 or keyword_count < 3 or (not has_email and not has_phone and len(found_skills) == 0):
            resume_obj.delete()
            return JsonResponse({
                'status': 'error',
                'message': 'AI Detection Alert: The uploaded file does not appear to be a valid resume. Please upload a professional resume containing your contact details, education, skills, and work experience.'
            }, status=400)
            
        resume_obj.extracted_text = text
        skills_str = ", ".join(found_skills) if found_skills else "Python, Django, SQL"
        
        history, created = UserHistory.objects.get_or_create(user=request.user)
        user_performance = history.avg_score or 80
        
        analysis = generate_career_analysis(skills_str, str(user_performance))
        
        ats_score = calculate_ats_score(text)
        resume_obj.skills = found_skills
        resume_obj.analysis_results = analysis
        resume_obj.ats_score = ats_score
        resume_obj.save()
        
        base_name = os.path.basename(resume_obj.file.name)
        clean_name = re.sub(r'_[a-zA-Z0-9]{7,10}(\.[a-zA-Z0-9]+)$', r'\1', base_name)
        
        return JsonResponse({
            'status': 'success',
            'analysis': analysis,
            'ats_score': ats_score,
            'filename': clean_name,
            'uploaded_at': resume_obj.uploaded_at.strftime('%b %d, %Y'),
            'resume_id': resume_obj.id,
            'extracted_text': text
        })
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def api_roadmap(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = generate_roadmap(data.get('goal', ''), data.get('skills', ''))
        return JsonResponse(result)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def appearance_view(request):
    theme_pref, created = ThemePreference.objects.get_or_create(user=request.user)
    return render(request, 'dashboard/appearance.html', {'current_theme': theme_pref.theme_name})

@login_required
def api_save_theme(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            theme_name = data.get('theme', 'default')
            if theme_name in ['default', 'corporate', 'executive', 'neural']:
                theme_pref, created = ThemePreference.objects.get_or_create(user=request.user)
                theme_pref.theme_name = theme_name
                theme_pref.save()
                return JsonResponse({'status': 'success', 'theme': theme_name})
            return JsonResponse({'status': 'error', 'message': 'Invalid theme name'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

