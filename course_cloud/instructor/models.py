from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Max,Min


class User(AbstractUser):
    role_options=[
        ("instructor","instructor"),
        ("Student","Student"),
    ]
    role=models.CharField(max_length=20,choices=role_options,default="Student")


class InstructorProfile(models.Model):
    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="instructor_profile")
    expertise=models.CharField(max_length=100,null=True)
    picture=models.ImageField(upload_to="instructor_profile_picture",default="instructor_profile_picture/default.png")
    about=models.TextField(null=True)
    def __str__(self):
        return self.owner.username
   

from django.db.models.signals import post_save

def create_insructor_profile(sender,instance,created,**kwargs):
    if created and instance.role=="instructor":
        InstructorProfile.objects.create(owner=instance)


post_save.connect(create_insructor_profile,User)

class Category(models.Model):
    name=models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Course(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(decimal_places=2,max_digits=7)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="instructor")
    is_free=models.BooleanField(default=False)
    picture=models.ImageField(upload_to="course_images",null=True,default="course_images/default_course.png")
    thumbnail=models.TextField()
    category_object=models.ManyToManyField(Category)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

class Module(models.Model):
    title=models.CharField(max_length=200)
    course_object=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="Module")
    order=models.PositiveIntegerField()

    def __str__(self):
        return f'{self.order}.{self.title}'
    
    def save(self,*args,**kwargs):
        max_order=Module.objects.filter(course_object=self.course_object).aggregate(max=Max("order")).get('max') or 0
        self.order=max_order+1
        super().save(*args,**kwargs)

    class Meta:
        ordering=["order"]  


class Lesson(models.Model):
    title=models.CharField(max_length=200)
    module_object=models.ForeignKey(Module,on_delete=models.CASCADE,related_name="lesson")
    vedio=models.TextField()
    order=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.module_object.title} + {self.title}"
    def save(self,*args,**kwargs):
        maxi_order=Lesson.objects.filter(module_object=self.module_object).aggregate(max=Max("order")).get('max') or 0
        self.order=maxi_order+1
        super().save(*args,**kwargs)
    class Meta:
        ordering=["order"]

    

