import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from resume.models import Resume

print("--- Resumes ---")
for r in Resume.objects.all():
    print(f"ID: {r.id} | User: {r.user.username} | File Name: {r.file.name} | URL: {r.file.url if r.file else 'None'}")
