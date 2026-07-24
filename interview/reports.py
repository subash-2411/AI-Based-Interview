from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse

def generate_interview_pdf(session):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title
    p.setFont("Helvetica-Bold", 20)
    p.drawString(100, height - 50, "AI Interview Performance Report")
    
    # User Info
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 100, f"User: {session.user.username}")
    p.drawString(100, height - 120, f"Date: {session.created_at.strftime('%Y-%m-%d %H:%M')}")
    p.drawString(100, height - 140, f"Language: {session.language}")
    p.drawString(100, height - 160, f"Overall Score: {session.score:.1f}%")
    
    p.line(100, height - 180, 500, height - 180)
    
    # Questions
    y = height - 210
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "Questions & Answers")
    y -= 30
    
    for q in session.questions.all():
        if y < 100: # New page
            p.showPage()
            y = height - 50
            
        p.setFont("Helvetica-Bold", 11)
        p.drawString(100, y, f"Q: {q.question_text}")
        y -= 20
        p.setFont("Helvetica", 10)
        p.drawString(120, y, f"Your Answer: {q.user_answer[:80]}...")
        y -= 20
        p.drawString(120, y, f"Score: {q.score:.0f}/100")
        y -= 15
        p.drawString(120, y, f"Feedback: {q.feedback}")
        y -= 40
        
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer

def download_report_view(request, session_id):
    from .models import InterviewSession
    session = InterviewSession.objects.get(id=session_id, user=request.user)
    pdf_buffer = generate_interview_pdf(session)
    
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="interview_report_{session_id}.pdf"'
    return response
