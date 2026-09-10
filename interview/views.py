from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import InterviewSession, InterviewQuestion
from resume.models import Resume
from ai_engine.logic import generate_questions, get_fallback_questions
import json
from django.http import JsonResponse

COMPANIES = ['General', 'TCS', 'Infosys', 'Wipro', 'Zoho', 'Accenture', 'HCL', 'Google', 'Amazon', 'Microsoft']

@login_required
def start_interview_view(request):
    # Temp migration runner inside view to guarantee column creation
    from django.core.management import call_command
    try:
        call_command('makemigrations', 'interview', interactive=False)
        call_command('migrate', interactive=False)
    except Exception as e:
        print(f"Migration error: {e}")

    resumes = Resume.objects.filter(user=request.user)
    has_resume = resumes.exists()
    if not has_resume:
        messages.warning(request, "Please upload your resume first to practice a customized mock interview based on your skills!")
        return redirect('resume:upload_resume')
    resume = resumes.latest('uploaded_at')


    if request.method == 'POST':
        lang = request.POST.get('language', 'en-US')
        diff = request.POST.get('difficulty', 'Beginner')   # Default: Beginner

        # Create session — resume may be None for general interviews
        session = InterviewSession.objects.create(
            user=request.user,
            resume=resume,
            language=lang,
            difficulty=diff
        )

        # Use resume skills if available, else use general topics
        if resume and resume.skills:
            skill_context = resume.skills
        else:
            skill_context = "Python, Data Structures, Problem Solving, Communication, SQL"

        # Pre-generate questions
        try:
            qs = generate_questions(skill_context, language=lang, difficulty=diff)
            for text in qs:
                InterviewQuestion.objects.create(session=session, question_text=text)
        except Exception as e:
            print(f"Pre-generation failed: {e}")
            fallback = get_fallback_questions(skill_context, count=5, language=lang)
            for text in fallback:
                InterviewQuestion.objects.create(session=session, question_text=text)

        return redirect('interview:interview_room', session_id=session.id)

    return render(request, 'interview/start.html', {
        'resume': resume,
        'has_resume': has_resume,
        'companies': COMPANIES,
    })


@login_required
def interview_room_view(request, session_id):
    session = InterviewSession.objects.get(id=session_id, user=request.user)
    questions = session.questions.all()
    return render(request, 'interview/room.html', {
        'session': session,
        'questions': questions,
        'questions_json': json.dumps([q.question_text for q in questions])
    })


@login_required
def submit_answer_api(request, session_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        question_index = data.get('index')
        answer_text = data.get('answer')

        session = InterviewSession.objects.get(id=session_id, user=request.user)
        question = session.questions.all()[question_index]
        question.user_answer = answer_text
        question.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def upload_recording_api(request, session_id):
    if request.method == 'POST' and request.FILES.get('video_recording'):
        session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
        video_file = request.FILES['video_recording']
        session.video_recording.save(f"session_{session.id}_recording.webm", video_file)
        session.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


from ai_engine.evaluation import evaluate_session

@login_required
def generate_questions_api(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    questions = session.questions.all()
    if questions.exists():
        return JsonResponse({
            'status': 'success',
            'questions': [q.question_text for q in questions]
        })

    lang = session.language
    diff = session.difficulty
    resume = session.resume
    skill_context = (resume.skills if resume and resume.skills else
                     "Python, Problem Solving, Communication, Data Structures")

    qs = generate_questions(skill_context, language=lang, difficulty=diff)
    for text in qs:
        InterviewQuestion.objects.create(session=session, question_text=text)

    return JsonResponse({'status': 'success', 'questions': qs})


@login_required
def complete_interview_view(request, session_id):
    session = InterviewSession.objects.get(id=session_id, user=request.user)
    session.is_completed = True
    
    # Save duration in seconds
    duration_secs = request.GET.get('duration')
    if duration_secs:
        try:
            session.duration = int(duration_secs)
        except ValueError:
            pass
            
    try:
        evaluate_session(session)
    except Exception as e:
        print(f"Evaluation error: {e}")
    session.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == '1':
        return JsonResponse({
            'status': 'success',
            'redirect_url': reverse('interview:interview_result', args=[session.id])
        })

    return redirect('interview:interview_result', session_id=session.id)


@login_required
def interview_result_view(request, session_id):
    session = InterviewSession.objects.get(id=session_id, user=request.user)
    return render(request, 'interview/result.html', {'session': session})


@login_required
def quick_start_interview_view(request):
    resumes = Resume.objects.filter(user=request.user)
    has_resume = resumes.exists()
    if not has_resume:
        messages.warning(request, "Please upload your resume first to practice a customized mock interview based on your skills!")
        return redirect('resume:upload_resume')
    resume = resumes.latest('uploaded_at')

    lang = request.GET.get('lang', 'en-US')
    diff = request.GET.get('difficulty', 'Beginner')  # Default: Beginner

    session = InterviewSession.objects.create(
        user=request.user,
        resume=resume,
        language=lang,
        difficulty=diff
    )

    skill_context = (resume.skills if resume and resume.skills else
                     "Python, Problem Solving, Communication, Data Structures")

    try:
        qs = generate_questions(skill_context, language=lang, difficulty=diff)
        for text in qs:
            InterviewQuestion.objects.create(session=session, question_text=text)
    except Exception as e:
        print(f"Quick-start error: {e}")
        fallback = get_fallback_questions(skill_context, count=5, language=lang)
        for text in fallback:
            InterviewQuestion.objects.create(session=session, question_text=text)

    return redirect('interview:interview_room', session_id=session.id)
