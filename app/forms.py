from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserCreateFrom(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        error_messages={'unique': 'This email address is already in use.'}  # Specify the error message for uniqueness

    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Your password must be at least 8 characters long and contain special characters."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email
