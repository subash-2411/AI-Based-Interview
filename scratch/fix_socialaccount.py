import os
import sys
import django

# Add project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

print("=== Existing SocialApps in DB ===")
apps = list(SocialApp.objects.all())
for app in apps:
    print(f"ID: {app.id}, Provider: {app.provider}, Name: '{app.name}', Client ID: '{app.client_id}', Sites: {[s.id for s in app.sites.all()]}")

if len(apps) > 1:
    print("\nMultiple SocialApp objects found! Cleaning up duplicates...")
    # Keep only the first valid one or remove all if configured via settings.py
    # Let's see: if settings.py has SOCIALACCOUNT_PROVIDERS['google']['APP'], allauth recommends either using settings OR db, not multiple broken DB rows.
    # We can delete empty/duplicate ones:
    for app in apps[1:]:
        print(f"Deleting duplicate/extra SocialApp ID {app.id} ('{app.name}')...")
        app.delete()

    first_app = SocialApp.objects.first()
    if first_app:
        site = Site.objects.get_current()
        if site not in first_app.sites.all():
            first_app.sites.add(site)
        print(f"Kept SocialApp ID {first_app.id} linked to site {site.id} ({site.domain})")
elif len(apps) == 1:
    site = Site.objects.get_current()
    if site not in apps[0].sites.all():
        apps[0].sites.add(site)
    print(f"Single SocialApp present: ID {apps[0].id} linked to site {site.id}")
else:
    print("No DB SocialApps found.")

print("\nDone!")
