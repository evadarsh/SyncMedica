from django.urls import path,include
from Clinic import views
app_name = 'webclinic'
urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
    path('profile/',views.profile,name="profile"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('notification/',views.notification,name="notification"),
    path('clinicdoctors/',views.clinicdoctors,name="clinicdoctors"),
    path('deletedoctor/<str:id>',views.deletedoctor,name="deletedoctor"),
    path('consultingdetails/<str:id>',views.consultingdetails,name="consultingdetails"),
    path('deleteconsultingdetails/<str:id>',views.deleteconsultingdetails,name="deleteconsultingdetails"),
    path('updateconsultingdetails/<str:id>',views.updateconsultingdetails,name="updateconsultingdetails"),
]