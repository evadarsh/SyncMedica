from django.urls import path,include
from User import views
app_name = 'webuser'
urlpatterns = [
     path('homepage/',views.homepage,name="homepage"),
     path('profile/',views.profile,name="profile"),
     path('editprofile/',views.editprofile,name="editprofile"),
     path('changepassword/',views.changepassword,name="changepassword"),
     path('viewdoctors/<str:id>',views.viewdoctors,name="viewdoctors"),
     path('viewdetails/<str:id>',views.viewdetails,name="viewdetails"),
     path('searchclinic/',views.searchclinic,name="searchclinic"),
     path('lockprofile/',views.lockprofile,name="lockprofile"),
     path('unlockprofile/',views.unlockprofile,name="unlockprofile"),
     path('logout/',views.logout,name="logout"),
     path('ajaxclinic/',views.ajaxclinic,name="ajaxclinic"),  
     path('ajaxbooking/',views.ajaxbooking,name="ajaxbooking"),
]