from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter that gracefully handles multiple SocialApp records in DB or settings
    to prevent MultipleObjectsReturned exceptions.
    """
    def get_app(self, request, provider, client_id=None):
        try:
            return super().get_app(request, provider, client_id=client_id)
        except Exception:
            # If multiple apps exist, pick the first configured one instead of crashing
            apps = SocialApp.objects.filter(provider=provider)
            if client_id:
                apps = apps.filter(client_id=client_id)
            if apps.exists():
                return apps.first()
            raise
