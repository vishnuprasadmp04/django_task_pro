from django.contrib import admin
from instructor.models import User,Category,Course,Module,Lesson,InstructorProfile
# Register your models here.

admin.site.register(User)
admin.site.register(Category)

class CourseModel(admin.ModelAdmin):
    exclude=("owner",)
    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner=request.user
        return super().save_model(request, obj, form, change)

class LessonInLine(admin.TabularInline):
    model=Lesson
    extra=1
    exclude=("order",)
class ModuleModel(admin.ModelAdmin):
    inlines=[LessonInLine]
    exclude=["order"]

class ProfileModel(admin.ModelAdmin):
    exclude=("owner",)
    def get_queryset(self, request):
        return super().get_queryset(request).filter(owner=request.user)
    def has_add_permission(self, request):
        return False


admin.site.register(Course,CourseModel)

admin.site.register(Module,ModuleModel)
admin.site.register(Lesson)
admin.site.register(InstructorProfile,ProfileModel)


