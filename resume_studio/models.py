from django.db import models
from django.conf import settings

class ResumeTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50) # e.g. Modern, Minimal, ATS Friendly
    preview_image = models.ImageField(upload_to='resume_templates/', null=True, blank=True)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ResumeProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='studio_resumes')
    template = models.ForeignKey(ResumeTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100, default="Untitled Resume")
    
    # Personal Info
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    
    # Summary
    career_objective = models.TextField(blank=True)
    
    # Other sections stored as JSON or text blocks for simplicity
    skills = models.TextField(blank=True, help_text="Comma separated skills")
    education_data = models.JSONField(default=list, blank=True) # [{'degree': '', 'institution': '', 'year': ''}]
    experience_data = models.JSONField(default=list, blank=True) # [{'title': '', 'company': '', 'duration': '', 'desc': ''}]
    certifications_data = models.JSONField(default=list, blank=True)
    languages_data = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class ResumeProject(models.Model):
    resume = models.ForeignKey(ResumeProfile, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.name

class JobDescription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class ResumeScore(models.Model):
    resume = models.ForeignKey(ResumeProfile, on_delete=models.CASCADE, related_name='scores')
    ats_score = models.IntegerField(default=0)
    keyword_score = models.IntegerField(default=0)
    quality_score = models.IntegerField(default=0)
    missing_keywords = models.TextField(blank=True)
    weak_sections = models.TextField(blank=True)
    suggestions = models.TextField(blank=True)
    analyzed_at = models.DateTimeField(auto_now_add=True)

class ResumeMatch(models.Model):
    resume = models.ForeignKey(ResumeProfile, on_delete=models.CASCADE)
    job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    match_percentage = models.IntegerField(default=0)
    missing_skills = models.TextField(blank=True)
    missing_keywords = models.TextField(blank=True)
    suggestions = models.TextField(blank=True)
    matched_at = models.DateTimeField(auto_now_add=True)
