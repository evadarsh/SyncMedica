from django.urls import path,include
from Admin import views
app_name = 'webadmin'
urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
    path('registration/',views.registration,name="registration"),
    path('medicalofficerregistration/',views.medicalofficerregistration,name="medicalofficerregistration"),
    path('district/',views.district,name="district"),
    path('deletedistrict/<str:id>',views.deletedistrict,name="deletedistrict"),
    path('updatedistrict/<str:id>',views.updatedistrict,name="updatedistrict"),
    path('place/',views.place,name="place"),
    path('deleteplace/<str:id>',views.deleteplace,name="deleteplace"),
    path('updateplace/<str:id>',views.updateplace,name="updateplace"),
    path('department/',views.department,name="department"),
    path('deletedepartment/<str:id>',views.deletedepartment,name="deletedepartment"),
    path('updatedepartment/<str:id>',views.updatedepartment,name="updatedepartment"),
    path('time/',views.time,name="time"),
    path('deletetime/<str:id>',views.deletetime,name="deletetime"),
    path('updatetime/<str:id>',views.updatetime,name="updatetime"),
    path('day/',views.day,name="day"),
    path('deleteday/<str:id>',views.deleteday,name="deleteday"),
    path('updateday/<str:id>',views.updateday,name="updateday"),
    path('logout/',views.logout,name="logout"),
]