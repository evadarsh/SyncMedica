from django.urls import path,include
from MedicalOfficer import views
app_name = 'webmedicalofficer'
urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
    path('profile/',views.profile,name="profile"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('approvedoctor/',views.approvedoctor,name="approvedoctor"),
    path('acceptdoctor/<str:id>',views.acceptdoctor,name="acceptdoctor"),
]