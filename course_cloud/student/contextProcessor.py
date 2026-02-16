from student.models import Cart


def CartCount(request):
    if request.user.is_authenticated:
        count=Cart.objects.filter(user_object=request.user).count()
        return {"CartCount":count}
    return{"CartCount":0}
