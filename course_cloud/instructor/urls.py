from django.urls import path
from instructor.views import *



urlpatterns=[
    path('instructor-signup',InstructorSignupView.as_view(),name='Instructor')

]