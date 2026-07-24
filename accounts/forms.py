from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class StudentRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email Address'})
    )
    phone_number = forms.CharField(
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Mobile Number (optional)',
            'pattern': '[0-9+\\-\\s]{7,15}'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        if commit:
            user.save()
        return user


class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username / Email / Mobile',
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Username, Email or Mobile Number',
            'autocomplete': 'off'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Enter your password',
            'autocomplete': 'new-password'
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'phone_number', 'profile_pic']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-field'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field'}),
            'bio': forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
            'phone_number': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Mobile Number'}),
        }
