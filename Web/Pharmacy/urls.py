from django.urls import path,include
from Pharmacy import views
app_name = 'webpharmacy'
urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
    path('profile/',views.profile,name="profile"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('medicine/',views.medicine,name="medicine"),
    path('deletemedicine/<str:id>',views.deletemedicine,name="deletemedicine"),
    path('users/',views.users,name="users"),
    path('viewprescriptions/<str:id>',views.viewprescriptions,name="viewprescriptions"),
    path('ajaxsearch_patient/',views.ajaxsearch_patient,name="ajaxsearch_patient"),
    path('generatebill/<str:id>',views.generatebill,name="generatebill"),
    path('otpverification/<str:id>',views.otpverification,name="otpverification"),
    path('checkstatus/<str:id>',views.checkstatus,name="checkstatus"),
    path('ajaxaddbill/',views.ajaxaddbill,name="ajaxaddbill"),
    path('ajaxdeletebill/',views.ajaxdeletebill,name="ajaxdeletebill"),
    path('checkqty/',views.checkqty,name="checkqty"),
    path('ajaxsubmitbill/',views.ajaxsubmitbill,name="ajaxsubmitbill"),
    path('viewbills/<str:id>',views.viewbills,name="viewbills"),
]