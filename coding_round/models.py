from django.db import models
from accounts.models import User

class CodingProblem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, default='Medium')
    tags = models.CharField(max_length=200, default='General', help_text="Comma separated skills: Python, Array, etc.")
    language = models.CharField(max_length=50, default='Python')
    initial_code = models.TextField(default="def solution():\n    # Write your code here\n    pass")
    
    def __str__(self):
        return self.title

class CodingSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(CodingProblem, on_delete=models.CASCADE)
    user_code = models.TextField()
    score = models.FloatField(default=0.0)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"
