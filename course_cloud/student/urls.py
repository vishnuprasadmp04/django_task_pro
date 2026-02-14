from django.urls import path
from student.views import *

urlpatterns=[
    path('signup',StudentCreationView.as_view(),name="signup"),
    path('student-home',StudentHomeView.as_view(),name="home"),
    path('course-details/<int:pk>',CourseDetailView.as_view(),name="course"),
    path('AddtoCart/<int:pk>',AddtoCartView.as_view(),name="AddtoCart"),
    path("CartView", CartView.as_view(), name="cart"),
    path('delete-cart/<int:pk>',RemoveCartView.as_view(),name="delcart"),
    path('checkout',PlaceOrderView.as_view(),name='order'),
    path('My-courses',MyCoursesView.as_view(),name='Mycourses'),
    path('viewlesson/<int:pk>',ViewLessonView.as_view(),name="Lesson"),

]