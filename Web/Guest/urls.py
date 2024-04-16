from django.urls import path,include
from Guest import views
app_name = 'webguest'
urlpatterns = [
    path('userregistration/',views.userregistration,name="userregistration"),
    path('pharmacyregistration/',views.pharmacyregistration,name="pharmacyregistration"),
    path('doctorregistration/',views.doctorregistration,name="doctorregistration"),
    path('clinicregistration/',views.clinicregistration,name="clinicregistration"),
    path('login/',views.login,name="login"),
    path('ajaxplace/',views.ajaxplace,name="ajaxplace"),
    path('',views.index,name="index"),
    path('doctors/',views.doctors,name="doctors"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
]