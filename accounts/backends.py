from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Allows login with username, email OR mobile phone number.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        # Look up the user by username OR email OR phone_number
        try:
            user = User.objects.filter(
                Q(username__iexact=username) |
                Q(email__iexact=username) |
                Q(phone_number=username)
            ).first()
        except Exception:
            user = None

        if user:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        else:
            # Run the default password hasher once to reduce timing attacks
            User().set_password(password)

        return None
