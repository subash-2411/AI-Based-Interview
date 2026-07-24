import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.management import call_command

print("Running makemigrations...")
call_command('makemigrations', 'interview', interactive=False)

print("Running migrate...")
call_command('migrate', interactive=False)

print("Migrations completed successfully!")
