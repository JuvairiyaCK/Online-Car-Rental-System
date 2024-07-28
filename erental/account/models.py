from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.


class Car(models.Model):
       title=models.CharField(max_length=200)
       description=models.CharField(max_length=500)
       image=models.ImageField(upload_to="car_images")
       rent=models.IntegerField()
       options=(
        ("Calicut","Calicut"),
        ("Kochi","Kochi"),
        ("Trivandrum","Trivandrum"),
        ("Kannur","Kannur"),
        ("Bangalore","Bangalore"),
        ("Mangalore","Mangalore")
              )
       city=models.CharField(max_length=200,choices=options)
       isavailable=models.BooleanField(default=True)


class Booking(models.Model):
        user=models.ForeignKey(User,on_delete=models.CASCADE)
        car=models.ForeignKey(Car,on_delete=models.CASCADE)
        days=models.IntegerField()
        Pickup_date=models.DateField(null=False,default=date.today)
        phone=models.IntegerField()
        address=models.CharField(max_length=500)
        date=models.DateField(auto_now_add=True)
        options=(
           ("Booking confirmed","Booking confirmed"),
           ("Booking completed","Booking completed")
             )
        status=models.CharField(max_length=200,default="Booking confirmed",choices=options)


        @property
        def total_rent(self):
              tamount=self.car.rent*self.days
              return tamount
