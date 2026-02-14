from django import forms
from instructor.models import User
from django.contrib.auth.forms import UserCreationForm


class InstructorForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","email","username","password1","password2"]
    def save(self, commit = ...):
        user=super().save(commit=False)
        user.is_superuser=True
        user.is_staff=True
        user.is_active=True
        user.role="instructor"
        if commit:
            user.save()
        return user

    