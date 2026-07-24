from django.db import models
from accounts.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True)
    skills = models.JSONField(default=list)
    ats_score = models.FloatField(default=0.0)
    analysis_results = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        import os, re
        try:
            base_name = os.path.basename(self.file.name)
            clean_name = re.sub(r'_[a-zA-Z0-9]{7,10}(\.[a-zA-Z0-9]+)$', r'\1', base_name)
            return clean_name
        except Exception:
            return f"{self.user.username}'s Resume"
