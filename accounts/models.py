from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.username

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=0) # 0-100
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"

class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_interviews = models.IntegerField(default=0)
    avg_score = models.FloatField(default=0.0)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.user.username} History"

class ThemePreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='theme_preference')
    theme_name = models.CharField(max_length=50, default='default')
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.theme_name}"

