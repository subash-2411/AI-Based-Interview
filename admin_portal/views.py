from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Avg
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from datetime import timedelta
import json

from accounts.models import User, UserHistory, Skill
from resume.models import Resume
from interview.models import InterviewSession, InterviewQuestion
from coding_round.models import CodingProblem, CodingSubmission


# ════════════════════════════════════════════
#  LANDING PAGE — Command Center gate (public)
# ════════════════════════════════════════════
def admin_landing(request):
    """Shows the Command Center entry screen to everyone."""
    return render(request, 'admin_portal/landing.html')


# ════════════════════════════════════════════
#  ADMIN LOGIN / LOGOUT
# ════════════════════════════════════════════
def admin_login_view(request):
    """Custom admin login — superuser credentials only."""
    # Already authenticated superuser → go straight to dashboard
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin_portal:dashboard')

    error = None
    username_val = ''

    if request.method == 'POST':
        username_val = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username_val, password=password)

        if user is None:
            error = 'Invalid username or password. Please try again.'
        elif not user.is_superuser:
            error = 'Access denied. This portal is for superadmins only.'
        else:
            login(request, user)
            next_url = request.GET.get('next', '/admin-portal/dashboard/')
            return redirect(next_url)

    return render(request, 'admin_portal/login.html', {
        'error': error,
        'username': username_val,
    })


def admin_logout_view(request):
    """Log out from admin portal and return to landing."""
    logout(request)
    return redirect('admin_portal:landing')


# ════════════════════════════════════════════
#  SUPERUSER GUARD
# ════════════════════════════════════════════
def superuser_required(view_func):
    """Decorator — redirects to admin login if not an authenticated superuser."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/admin-portal/login/?next={request.path}')
        if not request.user.is_superuser:
            return redirect('admin_portal:login')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


@superuser_required
def admin_dashboard(request):
    """Main admin dashboard with live stats."""
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    # ── Stats ──
    total_users        = User.objects.count()
    new_users_week     = User.objects.filter(date_joined__gte=week_ago).count()
    active_users       = User.objects.filter(last_login__gte=week_ago).count()
    total_resumes      = Resume.objects.count()
    avg_ats            = Resume.objects.aggregate(avg=Avg('ats_score'))['avg'] or 0
    total_interviews   = InterviewSession.objects.count()
    completed_iv       = InterviewSession.objects.filter(is_completed=True).count()
    avg_score          = InterviewSession.objects.aggregate(avg=Avg('score'))['avg'] or 0
    total_submissions  = CodingSubmission.objects.count()
    total_problems     = CodingProblem.objects.count()

    # ── Recent Users ──
    recent_users = User.objects.order_by('-date_joined')[:8].values(
        'id', 'username', 'email', 'phone_number', 'date_joined', 'is_staff', 'last_login'
    )

    # ── Recent Interviews ──
    recent_interviews = InterviewSession.objects.select_related('user').order_by('-created_at')[:6]

    # ── Recent Resumes ──
    recent_resumes = Resume.objects.select_related('user').order_by('-uploaded_at')[:6]

    # ── Recent Submissions ──
    recent_submissions = CodingSubmission.objects.select_related('user', 'problem').order_by('-completed_at')[:6]

    # ── Chart: Users registered per day (last 7 days) ──
    user_chart = []
    for i in range(6, -1, -1):
        day = now - timedelta(days=i)
        count = User.objects.filter(
            date_joined__date=day.date()
        ).count()
        user_chart.append({
            'day': day.strftime('%a'),
            'count': count
        })

    # ── Top users by interview count ──
    top_users = User.objects.annotate(
        iv_count=Count('interviewsession')
    ).order_by('-iv_count')[:5].values('username', 'email', 'iv_count')

    context = {
        # Stats
        'total_users': total_users,
        'new_users_week': new_users_week,
        'active_users': active_users,
        'total_resumes': total_resumes,
        'avg_ats': round(avg_ats, 1),
        'total_interviews': total_interviews,
        'completed_iv': completed_iv,
        'avg_score': round(avg_score, 1),
        'total_submissions': total_submissions,
        'total_problems': total_problems,
        # Tables
        'recent_users': recent_users,
        'recent_interviews': recent_interviews,
        'recent_resumes': recent_resumes,
        'recent_submissions': recent_submissions,
        # Chart
        'user_chart': json.dumps(user_chart),
        'top_users': top_users,
    }
    return render(request, 'admin_portal/dashboard.html', context)


@superuser_required
def admin_users(request):
    """All users management page."""
    search = request.GET.get('q', '')
    filter_type = request.GET.get('filter', 'all')

    users = User.objects.all()

    if search:
        from django.db.models import Q
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(phone_number__icontains=search)
        )

    if filter_type == 'staff':
        users = users.filter(is_staff=True)
    elif filter_type == 'active':
        users = users.filter(is_active=True)
    elif filter_type == 'recent':
        week_ago = timezone.now() - timedelta(days=7)
        users = users.filter(date_joined__gte=week_ago)

    users = users.order_by('-date_joined')

    context = {
        'users': users,
        'search': search,
        'filter_type': filter_type,
        'total': users.count(),
    }
    return render(request, 'admin_portal/users.html', context)


@superuser_required
def admin_user_detail(request, user_id):
    """Individual user detail page."""
    user = get_object_or_404(User, id=user_id)
    resumes = Resume.objects.filter(user=user).order_by('-uploaded_at')
    interviews = InterviewSession.objects.filter(user=user).order_by('-created_at')
    submissions = CodingSubmission.objects.filter(user=user).select_related('problem').order_by('-completed_at')

    # Handle POST actions (toggle staff, delete, etc.)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'toggle_staff':
            user.is_staff = not user.is_staff
            user.save()
            return JsonResponse({'success': True, 'is_staff': user.is_staff})
        elif action == 'toggle_active':
            user.is_active = not user.is_active
            user.save()
            return JsonResponse({'success': True, 'is_active': user.is_active})
        elif action == 'delete_user':
            username = user.username
            user.delete()
            return JsonResponse({'success': True, 'deleted': username})

    context = {
        'target_user': user,
        'resumes': resumes,
        'interviews': interviews,
        'submissions': submissions,
        'resume_count': resumes.count(),
        'interview_count': interviews.count(),
        'submission_count': submissions.count(),
        'avg_interview_score': interviews.aggregate(avg=Avg('score'))['avg'] or 0,
    }
    return render(request, 'admin_portal/user_detail.html', context)


@superuser_required
def admin_interviews(request):
    """All interview sessions."""
    sessions = InterviewSession.objects.select_related('user').order_by('-created_at')[:50]
    context = {
        'sessions': sessions,
        'total': InterviewSession.objects.count(),
        'completed': InterviewSession.objects.filter(is_completed=True).count(),
        'avg_score': InterviewSession.objects.aggregate(avg=Avg('score'))['avg'] or 0,
    }
    return render(request, 'admin_portal/interviews.html', context)


@superuser_required
def admin_resumes(request):
    """All resumes."""
    resumes = Resume.objects.select_related('user').order_by('-uploaded_at')[:50]
    context = {
        'resumes': resumes,
        'total': Resume.objects.count(),
        'avg_ats': Resume.objects.aggregate(avg=Avg('ats_score'))['avg'] or 0,
    }
    return render(request, 'admin_portal/resumes.html', context)


@superuser_required
def admin_coding(request):
    """Coding problems & submissions."""
    problems = CodingProblem.objects.annotate(sub_count=Count('codingsubmission')).order_by('-sub_count')
    submissions = CodingSubmission.objects.select_related('user', 'problem').order_by('-completed_at')[:30]
    context = {
        'problems': problems,
        'submissions': submissions,
        'total_problems': CodingProblem.objects.count(),
        'total_submissions': CodingSubmission.objects.count(),
    }
    return render(request, 'admin_portal/coding.html', context)


@superuser_required
def admin_add_problem(request):
    """Add a new coding problem."""
    if request.method == 'POST':
        try:
            CodingProblem.objects.create(
                title=request.POST.get('title', ''),
                description=request.POST.get('description', ''),
                difficulty=request.POST.get('difficulty', 'Medium'),
                tags=request.POST.get('tags', 'General'),
                language=request.POST.get('language', 'Python'),
                initial_code=request.POST.get('initial_code', 'def solution():\n    pass'),
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'error': 'POST only'}, status=405)


@superuser_required
def admin_delete_problem(request, problem_id):
    """Delete a coding problem."""
    if request.method == 'POST':
        problem = get_object_or_404(CodingProblem, id=problem_id)
        problem.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'POST only'}, status=405)


# ── AJAX Stats endpoint ──
@superuser_required
def admin_stats_api(request):
    """Live stats API for dashboard refresh."""
    return JsonResponse({
        'total_users': User.objects.count(),
        'total_interviews': InterviewSession.objects.count(),
        'total_resumes': Resume.objects.count(),
        'total_submissions': CodingSubmission.objects.count(),
        'avg_ats': round(Resume.objects.aggregate(avg=Avg('ats_score'))['avg'] or 0, 1),
        'avg_score': round(InterviewSession.objects.aggregate(avg=Avg('score'))['avg'] or 0, 1),
    })

from django.http import FileResponse, Http404
import os
import re

@superuser_required
def admin_download_resume(request, resume_id):
    """Securely download the correct resume file from storage."""
    resume = get_object_or_404(Resume, id=resume_id)
    if not resume.file:
        raise Http404("Resume file not found.")
    
    file_path = resume.file.path
    if not os.path.exists(file_path):
        raise Http404("File does not exist on disk.")
        
    # Read the file and serve it
    response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
    
    # Process original clean filename
    base_name = os.path.basename(resume.file.name)
    clean_name = re.sub(r'_[a-zA-Z0-9]{7,10}(\.[a-zA-Z0-9]+)$', r'\1', base_name)
    response['Content-Disposition'] = f'attachment; filename="{clean_name}"'
    return response
