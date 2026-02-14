from django.db import models
from instructor.models import User,Course
# Create your models here.
  

class Cart(models.Model):
    course_object=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="cart_course")
    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="cart_course_user")
    added_at=models.DateTimeField(auto_now_add=True)

class Wishlist(models.Model):
    course_object=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="wishlist_course")
    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="wishlist_course_user")
    added_at=models.DateTimeField(auto_now_add=True)
    
        
class Order(models.Model):
    course_object=models.ManyToManyField(Course,related_name="enrolled_course")
    student=models.ForeignKey(User,on_delete=models.CASCADE,related_name="purchase")
    is_paid=models.BooleanField(default=False)
    razr_par_order_id=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    total=models.DecimalField(max_digits=10,decimal_places=2)