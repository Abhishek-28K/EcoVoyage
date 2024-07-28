from django.shortcuts import render

# Create your views here.
def landingpage(request):
    return render(request,'authapp/home.html')

def loginpage(request):
    return render(request,'authapp/login.html')