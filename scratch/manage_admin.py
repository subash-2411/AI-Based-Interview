import os
import sys
import pathlib
import django

# Add project root directory to python path
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User

username_target = 'Subash'
password_target = '2411'

try:
    # Check if user already exists
    user = User.objects.filter(username__iexact=username_target).first()
    if user:
        print(f"User '{user.username}' found. Promoting to superuser and setting password to '{password_target}'...")
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password_target)
        user.save()
        print("Success! User promoted.")
    else:
        print(f"User '{username_target}' not found. Creating new superuser...")
        user = User.objects.create_superuser(
            username=username_target,
            email='subash@example.com',
            password=password_target
        )
        print(f"Success! Superuser '{username_target}' created with password '{password_target}'.")
except Exception as e:
    print(f"Error: {e}")
