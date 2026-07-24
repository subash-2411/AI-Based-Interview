import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User

# List all users
users = User.objects.all()
print("Existing users:")
for u in users:
    print(f"Username: {u.username}, Email: {u.email}, Superuser: {u.is_superuser}, Staff: {u.is_staff}")

# Let's see if there is an admin user.
admin_user = User.objects.filter(is_superuser=True).first()
if admin_user:
    print(f"\nSuperuser already exists: {admin_user.username}")
else:
    print("\nNo superuser found.")
