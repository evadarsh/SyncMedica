from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wadmin/',include('Admin.urls')),
    path('',include('Guest.urls')),
    path('medicalofficer/',include('MedicalOfficer.urls')),
    path('pharmacy/',include('Pharmacy.urls')),
    path('clinic/',include('Clinic.urls')),
    path('doctor/',include('Doctor.urls')),
    path('user/',include('User.urls')),
]
