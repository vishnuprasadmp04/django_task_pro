from django.shortcuts import render,redirect
from django.views import View
from instructor.forms import *
from django.contrib import messages
# Create your views here.


class InstructorSignupView(View):
    def get(self,request,*args,**kwargs):
        form=InstructorForm()
        return render(request,"instructor_signup.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form_data=InstructorForm(data=request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,"Instructor Signup successfull!!")
            return redirect('Instructor')
        return render(request,"instructor_signup.html",{"form":form_data})    
        
    
