from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,DetailView
from account.models import Car,Booking
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.info(request,"Please login First!!")
            return redirect('log')
    return inner
    
decorators=[signin_required,never_cache]


# Create your views here.
@method_decorator(decorators,name='dispatch')
class HomeView(TemplateView):
    template_name="home.html"


@method_decorator(decorators,name='dispatch')
class CarView(ListView):
    template_name="cars.html"
    queryset=Car.objects.all()
    context_object_name="data"
         
    def get_queryset(self):
        qs=super().get_queryset()
        qs=qs.filter(city=self.kwargs.get('plc'))
        return(qs)


@method_decorator(decorators,name='dispatch')
class CarDetailsView(DetailView):
    template_name="details.html"
    queryset=Car.objects.all()
    pk_url_kwarg="cid"
    context_object_name="car"



@method_decorator(decorators,name='dispatch')
class CheckoutView(TemplateView):
    template_name="checkout.html"
    
    def post(self,request,*args,**kwargs):
        try:
            cid=kwargs.get('cid')
            car=Car.objects.get(id=cid)
            user=request.user
            dys=request.POST.get('days')
            ph=request.POST.get('phone')
            addr=request.POST.get('address')
            pickup=request.POST.get('Pickup_date')
            subject="Booking Confirmation"
            msg=f"Your Booking for {car.title} is successfull"
            fr_om="dummy@example.com"
            to_ad=[user.email]
            send_mail(subject,msg,fr_om,to_ad)
            car.isavailable=False
            car.save()
            Booking.objects.create(car=car,user=user,days=dys,phone=ph,address=addr,Pickup_date=pickup)
            messages.success(request,"Booked successfully!!")
            return redirect('chome')
        except Exception as e:
            print(e)
            messages.error(request,"Something went wrong!!Order placing failed!!")
            return redirect('cdet')



@method_decorator(decorators,name='dispatch')
class BookingListView(ListView):
    template_name="bookinglist.html"
    queryset=Booking.objects.all()
    context_object_name="reserve"

    def get_queryset(self):
        qs=super().get_queryset()
        qs=qs.filter(user=self.request.user)
        return qs


decorators
def CancelBooking(request,*args,**kwargs):
    try:
        bid=kwargs.get('bid')
        book=Booking.objects.get(id=bid)
        subject="Booking Cancelling Acknowledgment"
        msg=f"Your Booking for {book.car.title} is successfully Cancelled"
        fr_om="dummy@example.com"
        to_ad=[request.user.email]
        send_mail(subject,msg,fr_om,to_ad)
        book.car.isavailable=True
        book.car.save()
        book.delete()
        messages.success(request,"Booking Cancelled!!")
        return redirect('blist')
    except Exception as e:
        messages.error(request,e)
        return redirect('blist')


    