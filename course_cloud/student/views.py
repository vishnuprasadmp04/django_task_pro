from django.shortcuts import render,redirect
from django.views import View
from student.forms import *
from django.views.generic import TemplateView,CreateView,FormView,ListView,DetailView
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login
from django.contrib import messages
from instructor.models import *
from student.models import *
import razorpay
# Create your views here.


RAZR_KEY_ID="rzp_test_SFy9f2Wfo8Y5Jj"
RAZR_SECRET_KEY="1mp2v9PT9unb14VrE2DPWscI"

class StudentCreationView(CreateView):
    template_name="student_Registration.html"
    form_class=StudentCreationForm
    success_url=reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request,"user signup successfully!")
        return super().form_valid(form)

class StudentLoginView(FormView):
    template_name="student_login.html"
    form_class=StudentLoginForm

    def post(self,request,*args,**kwargs):
        form_data=StudentLoginForm(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get('username')
            pswd=form_data.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            if user:
                login(request,user)
                print(user.role)
                if user.role=="Student":
                    return redirect('home')
                elif user.role=="instructor":
                    return redirect(reverse("admin:index"))
            
            else:
                messages.warning(request,"Invalid cridentials!!")
                return redirect('login')
        print("form invalid")
        return render(request,"student_login.html",{"form":form_data})


# class StudentHomeView(ListView):
#     template_name="student_home.html"
#     queryset=Course.objects.all()
#     context_object_name="course"
        
class StudentHomeView(ListView):
    def get(self,request,**kwargs):
        allcourses_qs=Course.objects.all()
        purchaced=Order.objects.filter(student=request.user,is_paid=True).values_list("course_object",flat=True)
        print(purchaced)
        return render(request,"student_home.html",{"course":allcourses_qs,"purchased_courses":purchaced})
    
    
class CourseDetailView(DetailView):
    template_name="coursedetails.html"
    queryset=Course.objects.all()
    context_object_name="course"


class AddtoCartView(View):
    def get(self,request,**kwargs):
        cid=kwargs.get('pk')
        course=Course.objects.get(id=cid)
        user=request.user
       
        try:
            Cart.objects.get_or_create(course_object=course,user_object=user)
            

            return redirect('home')
        except Exception as e:
            print(e) 
            # print('Already added to the cart')
            messages.info(request,"course Already added to cart!!!!!")
            return redirect('course',pk=cid)
class CartView(View):
    def get(self,request,**kwargs):
        qs=Cart.objects.filter(user_object=request.user)
        cart_total=0
        for i in qs:
            cart_total+=i.course_object.price
        return render(request,"cartsummary.html",{"data":qs,"cart_total":cart_total})
#     template_name="cartsummary.html"

class RemoveCartView(View):
    def get(self,request,**kwargs):
        cart_id=kwargs.get('pk')
        Cart.objects.get(id=cart_id).delete()
        return redirect('Cart')

class PlaceOrderView(View):
    def get(self,request):
        qs=Cart.objects.filter(user_object=request.user)
        student=request.user
        cart_total=0
        for i in qs:
            cart_total+=i.course_object.price
        order=Order.objects.create(student=student,total=cart_total)
        for i in qs:
            order.course_object.add(i.course_object)
        qs.delete()
        if cart_total>0:
            client = razorpay.Client(auth=(RAZR_KEY_ID,RAZR_SECRET_KEY))
            data = { "amount": int(cart_total*100), "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data)
            print(payment,"++++++++++++")
            order.razr_pay_order_id=payment.get('id')
            order.save()
            context={
                "razr_key_id":RAZR_KEY_ID,
                "amount":int(cart_total*100),
                "display_amount":cart_total,
                "razr_pay_id":payment.get('id')
            }
            print(cart_total)
            return render(request,"payment.html",{"data":context})
        return redirect('home')
    
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
@method_decorator(csrf_exempt,name="dispatch")
class PaymentVerifyView(View):

    def post(self, request):
        print(request.POST)   # check Razorpay response
        client = razorpay.Client(auth=(RAZR_KEY_ID, RAZR_SECRET_KEY))
        try:
            client.utility.verify_payment_signature(request.POST):
            razr_pay_order_id = request.POST.get('razorpay_order_id')
            order_instance=Order.objects.get(razr_pay_order_id=razr_pay_order_id)
            order_instance.is_paid=True
            order_instance.save()
        except:
            print("failed")
        return redirect('home')
        
class MyCoursesView(View):
   def get(self,request,**kwargs):
       qs=Order.objects.filter(student=request.user,is_paid=True)
       return render(request,"My-Courses.html",{"courses":qs})
   
class ViewLessonView(View):
   def get(self,request,**kwargs):
       course=Order.objects.filter(id=kwargs.get('pk'))
       query_params=request.GET
       module_id=query_params.get('module') if 'module' in query_params else Module.objects.filter(course_object=course).first().id
       module_object=Module.objects.get(id=module_id,course_object=course)

       lesson_id=query_params.get('lesson') if 'lesson' in query_params else Lesson.objects.filter(module_object=module_object).first().id
       lesson=Lesson.objects.get(id=lesson_id,module_object=module_object)
    #    if "module" in query_params:
    #        module_id=query_params.get('module')
    #    else:
    #        module_id=Module.objects.filter(course_object=course).first().id
       
    #    if "lesson" in query_params:
    #        lesson_id=query_params.get('lesson')
    #    else:
    #        lesson_id=Module.objects.all().first().id
        #    lesson_object=Lesson.objects.get(id=lesson_id,module_object=course)
 
       return render(request,"viewlesson.html",{"course":course,"lesson":lesson})