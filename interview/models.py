from django.db import models
from accounts.models import User
from resume.models import Resume

class InterviewSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.SET_NULL, null=True, blank=True)
    language = models.CharField(max_length=10, default='en-US')
    difficulty = models.CharField(max_length=20, default='Beginner')
    score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    video_recording = models.FileField(upload_to='interviews/', null=True, blank=True)
    duration = models.IntegerField(default=0)

    @property
    def formatted_duration(self):
        mins = self.duration // 60
        secs = self.duration % 60
        if mins > 0:
            return f"{mins}m {secs}s"
        return f"{secs}s"
    
    def __str__(self):
        return f"{self.user.username} - {self.language} Session"

class InterviewQuestion(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    ideal_answer = models.TextField(blank=True)
    user_answer = models.TextField(blank=True)
    score = models.FloatField(default=0.0)
    feedback = models.TextField(blank=True)
    
    def __str__(self):
        return f"Q for {self.session.id}"
