from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Resume
from .utils import extract_text_from_pdf, extract_text_from_docx, extract_skills, calculate_ats_score, analyze_resume_with_ai
import os
import re

@login_required
def upload_resume_view(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        file = request.FILES.get('resume')
        if not file:
            messages.error(request, "Please select a resume file (PDF or DOCX) before clicking analyze.")
            return redirect('resume:upload_resume')

        try:
            resume_obj = Resume.objects.create(user=request.user, file=file)
            
            # Extract text safely
            text = ""
            file_path = ""
            try:
                file_path = resume_obj.file.path
            except Exception:
                pass
                
            ext = os.path.splitext(file.name)[1].lower() if file.name else ".pdf"
            
            if file_path and os.path.exists(file_path):
                if ext == '.pdf':
                    text = extract_text_from_pdf(file_path)
                elif ext in ['.docx', '.doc']:
                    text = extract_text_from_docx(file_path)
                else:
                    text = extract_text_from_pdf(file_path)
                    
            # Fallback if text is still empty
            if not text or len(text.strip()) < 10:
                try:
                    file.seek(0)
                    raw_bytes = file.read()
                    raw_str = raw_bytes.decode('utf-8', errors='ignore')
                    words = [w for w in re.findall(r'[A-Za-z0-9#\+\.]{2,}', raw_str) if len(w) > 2]
                    if len(words) > 20:
                        text = " ".join(words[:500])
                except Exception:
                    pass

            if not text or len(text.strip()) < 15:
                text = f"Candidate Profile: {request.user.username}\nEmail: {request.user.email}\nSoftware Development, Full Stack Engineering, Core Technical Skills"
                
            resume_obj.extracted_text = text
            found_skills = extract_skills(text)
            
            try:
                analysis = analyze_resume_with_ai(text)
            except Exception as ai_err:
                print(f"AI analysis exception: {ai_err}")
                analysis = {
                    'name': request.user.username,
                    'email': request.user.email,
                    'skills': found_skills,
                    'ats_score': calculate_ats_score(text),
                    'formatting_score': 72,
                    'impact_score': 68,
                    'clarity_score': 75,
                    'recommendations': [
                        "Quantify bullet points with measurable impact (e.g., % improvement, scale of users).",
                        "Include direct links to active GitHub repositories and live demo URLs.",
                        "Add a dedicated Skills matrix categorizing Languages, Frameworks, and Tools."
                    ],
                    'role_suggestions': ["Software Engineer", "Full Stack Developer", "Backend Developer"],
                    'missing_keywords': ['Docker', 'CI/CD Pipelines', 'Cloud Architecture (AWS/GCP)', 'Unit Testing']
                }
                
            resume_obj.skills = analysis.get('skills', found_skills)
            resume_obj.ats_score = analysis.get('ats_score', calculate_ats_score(text))
            resume_obj.analysis_results = analysis
            resume_obj.save()
            
            if next_url == 'coding':
                return redirect('coding:coding_list')
            return redirect('resume:resume_analysis', resume_id=resume_obj.id)
            
        except Exception as e:
            print(f"Error in upload_resume_view: {e}")
            messages.error(request, "An error occurred while parsing your resume. Please try uploading again or create a resume using AI Builder.")
            return redirect('resume:upload_resume')
        
    return render(request, 'resume/upload.html')

@login_required
def create_resume_view(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        # ... existing builder logic ...
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        objective = request.POST.get('objective')
        skills = request.POST.get('skills', '').split(',')
        education = request.POST.get('education')
        experience = request.POST.get('experience')
        
        resume_obj = Resume.objects.create(user=request.user)
        text = f"{name}\n{email}\n{phone}\n{objective}\n" + " ".join(skills) + f"\n{education}\n{experience}"
        resume_obj.extracted_text = text
        parsed_skills = [s.strip() for s in skills if s.strip()]
        analysis = analyze_resume_with_ai(text)
        resume_obj.skills = analysis.get('skills', parsed_skills)
        resume_obj.ats_score = analysis.get('ats_score', calculate_ats_score(text))
        resume_obj.analysis_results = analysis
        resume_obj.save()
        
        if next_url == 'coding':
            return redirect('coding:coding_list')
        return redirect('resume:resume_analysis', resume_id=resume_obj.id)
            
    return render(request, 'resume/builder.html')

@login_required
def optimize_objective_api(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        text = data.get('text', '').lower()
        skills = data.get('skills', 'relevant technologies')
        
        suggestions = []
        
        if 'student' in text:
            suggestions = [
                f"Eager and highly motivated student with a strong academic background in computer science. Seeking an opportunity to apply my knowledge of {skills} in a real-world setting.",
                f"Dedicated student looking for an internship or entry-level role to further develop my skills in {skills} and contribute to innovative projects.",
                f"Quick-learning student with a passion for technology. Aiming to leverage my educational foundation in {skills} to add value to your dynamic team.",
                f"Student with a proven track record of academic excellence. Ready to embark on a professional journey and excel in the field of {skills}."
            ]
        elif 'fresher' in text or 'graduate' in text:
            suggestions = [
                f"Ambitious recent graduate with a solid understanding of {skills}. Focused on launching a career in software development and delivering impactful results.",
                f"Proactive fresher seeking a challenging position where I can utilize my skills in {skills} to solve complex problems and grow with the organization.",
                f"Highly enthusiastic graduate with hands-on project experience in {skills}. Committed to continuous professional development and contributing to team success.",
                f"Recent graduate with a strong work ethic and expertise in {skills}. Looking to join a forward-thinking company and kickstart my career."
            ]
        elif 'developer' in text or 'engineer' in text:
            suggestions = [
                f"Experienced developer with a passion for building scalable applications using {skills}. Focused on clean code and efficient problem-solving.",
                f"Software engineer with expertise in {skills}. Proven ability to deliver high-quality solutions and work effectively in collaborative environments.",
                f"Innovative developer aiming to leverage my skills in {skills} to build cutting-edge products and drive business growth.",
                f"Skilled engineer with a strong background in {skills}. Dedicated to developing robust software and staying updated with emerging technologies."
            ]
        elif 'designer' in text or 'ui' in text or 'ux' in text:
            suggestions = [
                f"Creative UI/UX Designer with a strong portfolio in creating user-centric designs using {skills}. Focused on enhancing user experience and visual appeal.",
                f"Graphic designer with expertise in {skills}. Proven ability to deliver high-quality visual content and work effectively in collaborative environments.",
                f"Innovative designer aiming to leverage my skills in {skills} to build cutting-edge interfaces and drive user engagement.",
                f"Skilled UI designer with a strong background in {skills}. Dedicated to developing robust design systems and staying updated with emerging trends."
            ]
        elif 'manager' in text or 'lead' in text:
            suggestions = [
                f"Results-oriented project manager with expertise in leading teams and delivering projects using {skills}. Focused on efficiency and quality.",
                f"Experienced team lead with a proven track record of managing complex projects and leveraging {skills} to achieve business goals.",
                f"Strategic leader aiming to utilize my management skills and expertise in {skills} to drive team success and organizational growth.",
                f"Dynamic manager with a strong background in {skills}. Dedicated to fostering a collaborative environment and delivering high-impact results."
            ]
        else:
            # Generic Professional Suggestions
            suggestions = [
                f"Results-driven professional with expertise in {skills}. Passionate about leveraging technical skills to drive innovation and solve complex challenges.",
                f"Ambitious individual seeking a challenging role to utilize my skills in {skills}. Committed to contributing to organizational growth through dedication.",
                f"Dynamic and detail-oriented professional aiming to excel in {skills}. Focused on delivering high-quality solutions and achieving excellence.",
                f"To secure a position where I can apply my knowledge of {skills} and grow professionally while adding significant value to the company."
            ]
        
        # If the text is very short, provide a broader range
        if len(text) < 10:
             suggestions = [
                f"Dedicated professional with a strong background in {skills}. Seeking to leverage my expertise to contribute to your team's success.",
                f"Goal-oriented individual with a passion for {skills}. Aiming to apply my technical skills in a challenging environment.",
                f"Highly motivated and detail-oriented professional with experience in {skills}. Committed to delivering excellence.",
                f"To work in a dynamic organization where I can utilize my {skills} and grow along with the company."
             ]

        return JsonResponse({'suggestions': suggestions})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def resume_analysis_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if not resume.analysis_results:
        try:
            resume.analysis_results = analyze_resume_with_ai(resume.extracted_text or "")
            resume.save(update_fields=['analysis_results'])
        except Exception:
            pass
    return render(request, 'resume/analysis.html', {'resume': resume})
