from django.urls import path,include
from Doctor import views
app_name = 'webdoctor'
urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
    path('profile/',views.profile,name="profile"),
    path('logout/',views.logout,name="logout"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('clinicrequests/',views.clinicrequests,name="clinicrequests"),
    path('consultingdeatils/',views.consultingdeatils,name="consultingdeatils"), 
    path('viewdetails/<str:id>',views.viewdetails,name="viewdetails"),
    path('appointments/<str:id>',views.appointments,name="appointments"),
    path('prescription/<str:id>',views.prescription,name="prescription"),  
    path('updateclinic/<str:id>',views.updateclinic,name="updateclinic"),  
    path('rejectclinic/<str:id>',views.rejectclinic,name="rejectclinic"), 
]
