from django.urls import path,include
from MedicalOfficer import views
app_name = 'webmedicalofficer'
urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
    path('profile/',views.profile,name="profile"),
    path('editprofile/',views.editprofile,name="editprofile"),
    path('changepassword/',views.changepassword,name="changepassword"),
    path('approvedoctor/',views.approvedoctor,name="approvedoctor"),
    path('accepteddoctorslist/',views.accepteddoctorslist,name="accepteddoctorslist"),
    path('rejecteddoctorslist/',views.rejecteddoctorslist,name="rejecteddoctorslist"),
    path('acceptdoctor/<str:id>',views.acceptdoctor,name="acceptdoctor"),
    path('rejectdoctor/<str:id>',views.rejectdoctor,name="rejectdoctor"),
    path('approveclinic/',views.approveclinic,name="approveclinic"),
    path('acceptedclinicslist/',views.acceptedclinicslist,name="acceptedclinicslist"),
    path('rejectedclinicslist/',views.rejectedclinicslist,name="rejectedclinicslist"),
    path('acceptclinic/<str:id>',views.acceptclinic,name="acceptclinic"),
    path('rejectclinic/<str:id>',views.rejectclinic,name="rejectclinic"),
    path('approvepharmacy/',views.approvepharmacy,name="approvepharmacy"),
    path('acceptedpharmacieslist/',views.acceptedpharmacieslist,name="acceptedpharmacieslist"),
    path('rejectedpharmacieslist/',views.rejectedpharmacieslist,name="rejectedpharmacieslist"),
    path('acceptpharmacy/<str:id>',views.acceptpharmacy,name="acceptpharmacy"),
    path('rejectpharmacy/<str:id>',views.rejectpharmacy,name="rejectpharmacy"),
]