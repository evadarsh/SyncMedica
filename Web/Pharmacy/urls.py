from django.urls import path,include
from Pharmacy import views
app_name = 'webpharmacy'
urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
    path('profile/',views.profile,name="profile"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('users/',views.users,name="users"),
    path('viewprescriptions/<str:id>',views.viewprescriptions,name="viewprescriptions"),
    path('ajaxsearch_patient/',views.ajaxsearch_patient,name="ajaxsearch_patient"),
    path('generatebill/<str:id>',views.generatebill,name="generatebill"),
    path('otpverification/<str:id>',views.otpverification,name="otpverification"),
    path('checkstatus/<str:id>',views.checkstatus,name="checkstatus"),
]