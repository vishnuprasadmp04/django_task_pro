from django import forms
from instructor.forms import User
from django.contrib.auth.forms import UserCreationForm


class StudentCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
class StudentLoginForm(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput())
    password=forms.CharField(max_length=100,widget=forms.PasswordInput())
