from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from authy.models import Profile


def invalid_user(value):
    """
    Checking symbol validation in username
    """
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError("This is an Invalid user, Do not user these chars: @, -, +")


def unique_user(value):
    """
    Checking user for uniqueness
    """
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError("User with this username already exists.")


def unique_email(value):
    """
    Checking email for uniqueness
    """
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError("User with this email already exists.")


class SignupForm(forms.ModelForm):
    """
    User registration form
    """
    MIN_LENGTH = 8

    username = forms.CharField(widget=forms.TextInput(), max_length=30, required=True)
    email = forms.CharField(widget=forms.EmailInput(), max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(invalid_user)
        self.fields['username'].validators.append(unique_user)
        self.fields['email'].validators.append(unique_email)

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if len(password) < self.MIN_LENGTH:
            raise forms.ValidationError(f"The password must be at least {self.MIN_LENGTH} characters long.")

        first_isalpha = password[0].isalpha()
        if all(a.isalpha() == first_isalpha for a in password):
            raise forms.ValidationError(
                "The password must contain at least one letter and at least one digit or punctuation character.")

        if password != confirm_password:
            self._errors['password'] = self.error_class(["Password don't match. Try again."])

        return self.cleaned_data


class ChangePasswordForm(forms.ModelForm):
    """
    User password change form
    """
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput(), label="Old password", required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(), label="New password", required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm new password", required=True)

    class Meta:
        model = User
        fields = ('id', 'old_password', 'new_password', 'confirm_password')

    def clean(self):
        super(ChangePasswordForm, self).clean()
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        user = User.objects.get(pk=id)
        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class(["Old password do not match."])
        if new_password != confirm_password:
            self._errors['new_password'] = self.error_class(["Passwords do not match."])
        return self.cleaned_data


class EditProfileForm(forms.ModelForm):
    """
    User profile change form
    """
    first_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    last_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    profile_info = forms.CharField(widget=forms.TextInput(), max_length=5000, required=False)
    picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'profile_info', 'picture')
