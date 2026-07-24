from django.db import models
from django.conf import settings

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Technical Round', 'Technical Round'),
        ('HR Round', 'HR Round'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Applied')
    applied_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.company} ({self.role})"

class LearningProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learning_progress')
    topic = models.CharField(max_length=100) # e.g., Python, DSA, Communication
    progress_percentage = models.IntegerField(default=0)
    xp_earned = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.topic} ({self.progress_percentage}%)"

class DailyChallenge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='daily_challenges')
    challenge_type = models.CharField(max_length=100) # e.g., Coding, Aptitude, Interview
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    xp_reward = models.IntegerField(default=10)
    assigned_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
