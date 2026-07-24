from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import ResumeTemplate, ResumeProfile, ResumeProject, JobDescription, ResumeScore, ResumeMatch
from resume.models import Resume
from resume.utils import extract_text_from_pdf, extract_text_from_docx, calculate_ats_score, analyze_resume_with_ai, extract_skills
from ai_engine.new_features import generate_job_match, improve_resume_text
import os
import json

@login_required
def dashboard(request):
    resumes = ResumeProfile.objects.filter(user=request.user).order_by('-updated_at')
    context = {
        'resumes': resumes
    }
    return render(request, 'resume_studio/dashboard.html', context)

@login_required
def resume_builder(request):
    # Get or create a profile; support multiple by template type
    template_id = request.GET.get('template', 'classic')
    profile, created = ResumeProfile.objects.get_or_create(
        user=request.user,
        title=f"Resume - {template_id.title()}"
    )
    context = {
        'profile': profile,
        'template_id': template_id,
    }
    return render(request, 'resume_studio/builder.html', context)

@login_required
def resume_preview(request):
    profile = ResumeProfile.objects.filter(user=request.user).first()
    context = {'profile': profile}
    return render(request, 'resume_studio/preview.html', context)

@login_required
def ats_checker(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        file = request.FILES['resume']
        ext = os.path.splitext(file.name)[1].lower()
        
        # Save temporary file to extract text
        temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media', 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file.name)
        
        with open(temp_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
                
        try:
            text = ""
            if ext == '.pdf':
                text = extract_text_from_pdf(temp_path)
            elif ext == '.docx':
                text = extract_text_from_docx(temp_path)
            elif ext == '.txt':
                with open(temp_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                    
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
            if not text.strip():
                return JsonResponse({'error': 'Could not extract text from file.'}, status=400)
                
            score = calculate_ats_score(text)
            found_skills = extract_skills(text)
            
            # Simple missing keywords check
            all_keywords = ['docker', 'ci/cd', 'aws', 'kubernetes', 'cloud', 'graphql', 'typescript', 'microservices', 'redis', 'testing']
            missing = [kw.title() for kw in all_keywords if kw not in text.lower()][:4]
            
            return JsonResponse({
                'status': 'success',
                'ats_score': score,
                'strong_keywords': found_skills[:8],
                'missing_keywords': missing
            })
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return JsonResponse({'error': str(e)}, status=500)
            
    return render(request, 'resume_studio/ats_checker.html')

@login_required
def resume_analyzer(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == '1':
        resume_id = request.GET.get('resume_id')
        if not resume_id:
            return JsonResponse({'error': 'No resume selected.'}, status=400)
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        return JsonResponse({
            'status': 'success',
            'name': resume.analysis_results.get('name', resume.user.username),
            'email': resume.analysis_results.get('email', resume.user.email),
            'phone': resume.analysis_results.get('phone', 'Not Found'),
            'objective': resume.analysis_results.get('objective', 'Not specified'),
            'formatting_score': resume.analysis_results.get('formatting_score', 80),
            'impact_score': resume.analysis_results.get('impact_score', 75),
            'clarity_score': resume.analysis_results.get('clarity_score', 85),
            'sections': resume.analysis_results.get('sections', {}),
            'recommendations': resume.analysis_results.get('recommendations', []),
        })
        
    resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'resume_studio/analyzer.html', {'resumes': resumes})

@login_required
def cover_letter_generator(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            resume_text = data.get('resume_text', '')
            job_title = data.get('job_title', '')
            company_name = data.get('company_name', '')
            job_desc = data.get('job_desc', '')
            
            from ai_engine.new_features import generate_cover_letter
            letter = generate_cover_letter(resume_text, job_title, company_name, job_desc)
            return JsonResponse({'status': 'success', 'letter': letter})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
    seen = set()
    unique_resumes = []
    for r in resumes:
        clean_name = str(r)
        if clean_name not in seen:
            seen.add(clean_name)
            unique_resumes.append(r)
            
    return render(request, 'resume_studio/cover_letter.html', {'resumes': unique_resumes})

@login_required
def ai_improver(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            if not text:
                return JsonResponse({'error': 'No text provided.'}, status=400)
            improved = improve_resume_text(text)
            return JsonResponse({'status': 'success', 'improved_text': improved})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return render(request, 'resume_studio/improver.html')

@login_required
def template_selection(request):
    return render(request, 'resume_studio/template_selection.html')

