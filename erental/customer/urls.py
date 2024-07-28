from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('chome',HomeView.as_view(),name='chome'),
    path('cars/<str:plc>',CarView.as_view(),name='cars'),
    path('cdet/<int:cid>',CarDetailsView.as_view(),name="cdet"),
    path('checkout/<int:cid>',CheckoutView.as_view(),name="cout"),
    path('bookinglist',BookingListView.as_view(),name="blist"),
    path('cancelbooking/<int:bid>',CancelBooking,name="cbook")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
