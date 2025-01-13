from django.shortcuts import render

# Create your views here.
def game(request):

    return render(request, "Bolts and Nuts.html",)

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        response = {"username": None, "msg": None}
        if form.is_valid():
            response["user"] = form.cleaned_data.get("user")
            print(form.cleaned_data)
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar_obj = request.FILES.get('avatar')
            '''初始代码
            if avatar_obj:
                user_obj=UserInfo.objects.create_user(username=user,password=pwd,email=email,avatar=avatar_obj)
            else:
                user_obj = UserInfo.objects.create_user(username=user, password=pwd, email=email)
            '''
            # 简化后的代码
            extra = {}
            if avatar_obj:
                extra['avatar'] = avatar_obj
            UserInfo.objects.create_user(username=user, password=pwd, email=email, **extra)
        else:
            # print(form.cleaned_data)
            # print(form.errors)
            response["msg"] = form.errors
        return JsonResponse(response)

    form = UserForm()
    return render(request, "register.html", {"form": form})
