from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import UserBase

# Login form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'login-pwd',
        }
    ))

# Creating an Account form
class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label='Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Please enter an email address'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    # To give an error if the username already exists.
    def clean_user_name(self):
        user_name = self.cleaned_data['user_name'].lower()
        u = UserBase.objects.filter(user_name=user_name)
        if u.count():
            raise forms.ValidationError("Username already exists")
        return user_name
    
    # Gives an error alert when the passwords don't match.
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd ['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    # Gives an error when there is already an account associated with a certain email.
    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another email, email already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control'})