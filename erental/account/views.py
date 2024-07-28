from django.forms import BaseModelForm
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import CreateView,TemplateView,FormView
from .forms import RegisterForm,LogForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.



class LandingView(TemplateView):
    template_name="index.html"


class LoginView(FormView):
    template_name="log.html"
    form_class=LogForm
    def post(self,request):
        form_data=LogForm(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get('username')
            pswd=form_data.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            if user:
                print(user)
                login(request,user)
                messages.success(request,"Login successful!!")
                return redirect('chome')
            else:
                print(user,"login failed")
                messages.error(request,"login failed")
                return redirect('log')
        return render(request,"log.html",{"form":form_data})
    # def get(self,request):


class RegView(CreateView):
    form_class=RegisterForm
    template_name="reg.html"
    success_url=reverse_lazy("log")
    def form_valid(self, form: BaseModelForm):
        messages.success(self.request,"Registration completed")
        return super().form_valid(form)
    def form_invalid(self, form: BaseModelForm):
        messages.error(self.request,"Registration failed")
        return super().form_invalid(form)



class LogOutView(View):
    def get(self,request):
        logout(request)
        return redirect('landing')