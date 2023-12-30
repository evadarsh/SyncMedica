from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import storage,auth,credentials,firestore
import pyrebase

config = {
  "apiKey": "AIzaSyC70VZNPMcg6Y2dRM3yqDa6u-jlD3kb5eg",
  "authDomain": "syncmedica-2000.firebaseapp.com",
  "projectId": "syncmedica-2000",
  "storageBucket": "syncmedica-2000.appspot.com",
  "messagingSenderId": "131644506908",
  "appId": "1:131644506908:web:2917e8b0fecd4a5d5430d9",
  "measurementId": "G-Y7PE5W8EXK",
  "databaseURL":"",
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
sd = firebase.storage()

db = firestore.client()

def homepage(request):
    admin = db.collection("tbl_admin").document(request.session["aid"]).get().to_dict()
    return render(request,"Admin/HomePage.html",{"admin":admin})

def registration(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            admin = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Admin/Registration.html",{"msg":error})

        image = request.FILES.get("txt_photo")
        if image:
            path = "Admin/Registration/" + image.name
            sd.child(path).put(image)
            download_url = sd.child(path).get_url(None)
        
        admin = {"admin_id":(admin.aid),
                "admin_name":request.POST.get("txt_name"),
                "admin_contact":request.POST.get("txt_contact"),
                "admin_email":request.POST.get("txt_email"),
                "admin_photo":(download_url),}
        db.collection("tbl_admin").add(admin)
        return redirect("webadmin:registration")
    else:
        return render(request,"Admin/Registration.html")

def medicalofficerregistration(request):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for i in dis:
        data = i.to_dict()
        dis_data.append({"district":data,"id":i.id})
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            medicalofficer = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Admin/MedicalOfficerRegistration.html",{"msg":error})

        image = request.FILES.get("txt_photo")
        if image:
            path = "Admin/MedicalOfficerRegistration/" + image.name
            sd.child(path).put(image)
            download_url = sd.child(path).get_url(None)
        
        medicalofficer = {"medicalofficer_id":(medicalofficer.aid),
                "medicalofficer_name":request.POST.get("txt_name"),
                "medicalofficer_district":request.POST.get("sel_district"),
                "medicalofficer_contact":request.POST.get("txt_contact"),
                "medicalofficer_email":request.POST.get("txt_email"),
                "medicalofficer_photo":(download_url),}
        db.collection("tbl_medicalofficer").add(medicalofficer)
        return redirect("webadmin:registration")
    else:
        return render(request,"Admin/MedicalOfficerRegistration.html",{"district":dis_data})

def district(request):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for i in dis:
        data = i.to_dict()
        dis_data.append({"district":data,"id":i.id})
    if request.method == "POST":
        data = {"district_name":request.POST.get("txt_district")}
        db.collection("tbl_district").add(data)
        return redirect("webadmin:district")
    else:
        return render(request,"Admin/District.html",{"dis":dis_data})
    
def deletedistrict(request,id):
    db.collection("tbl_district").document(id).delete()
    return redirect("webadmin:district")

def updatedistrict(request,id):
    dis = db.collection("tbl_district").document(id).get().to_dict()
    if request.method == "POST":
        data = {"district_name":request.POST.get("txt_district")}
        db.collection("tbl_district").document(id).update(data)
        return redirect("webadmin:district")
    else:
        return render(request,"Admin/District.html",{"district":dis})

def place(request):
    district = db.collection("tbl_district").stream()
    district_data = []
    for dis in district:
        district_data.append({"district":dis.to_dict(),"id":dis.id})
    plc = db.collection("tbl_place").stream()
    plc_data = []
    for s in plc:
        pdata = s.to_dict()
        dis_data = db.collection("tbl_district").document(pdata["district_id"]).get().to_dict()
        plc_data.append({"district":dis_data,"place":pdata,"id":s.id})
    if request.method == "POST":
        data = {"place_name":request.POST.get("txt_place"),"district_id":request.POST.get("sel_district")}
        db.collection("tbl_place").add(data)
        return redirect("webadmin:place")
    else:
        return render(request,"Admin/Place.html",{"dis":district_data,"plc":plc_data})

def deleteplace(request,id):
    db.collection("tbl_place").document(id).delete()
    return redirect("webadmin:place")

def updateplace(request,id):
    district = db.collection("tbl_district").stream()
    dist_data = []
    for c in district:
        dist_data.append({"district":c.to_dict(),"id":c.id})
    plc = db.collection("tbl_place").document(id).get().to_dict()
    if request.method == "POST":
        data = {"place_name":request.POST.get("txt_place"),"district_id":request.POST.get("sel_district")}
        db.collection("tbl_place").document(id).update(data)
        return redirect("webadmin:place")
    else:
        return render(request,"Admin/Place.html",{"place":plc,"dis":dist_data})

def department(request):
    dip = db.collection("tbl_department").stream()
    dip_data = []
    for i in dip:
        data = i.to_dict()
        dip_data.append({"department":data,"id":i.id})
    if request.method == "POST":
        data = {"department_name":request.POST.get("txt_department")}
        db.collection("tbl_department").add(data)
        return redirect("webadmin:department")
    else:
        return render(request,"Admin/Department.html",{"dip":dip_data})
    
def deletedepartment(request,id):
    db.collection("tbl_department").document(id).delete()
    return redirect("webadmin:department")

def updatedepartment(request,id):
    dip = db.collection("tbl_department").document(id).get().to_dict()
    if request.method == "POST":
        data = {"department_name":request.POST.get("txt_department")}
        db.collection("tbl_department").document(id).update(data)
        return redirect("webadmin:department")
    else:
        return render(request,"Admin/Department.html",{"department":dip})

def time(request):
    time = db.collection("tbl_time").stream()
    time_data = []
    for i in time:
        data = i.to_dict()
        time_data.append({"time":data,"id":i.id})
    if request.method == "POST":
        data = {"time_from":request.POST.get("txt_timefrom"),"time_to":request.POST.get("txt_timeto")}
        db.collection("tbl_time").add(data)
        return redirect("webadmin:time")
    else:
        return render(request,"Admin/time.html",{"time":time_data})

def deletetime(request,id):
    db.collection("tbl_time").document(id).delete()
    return redirect("webadmin:time")

def updatetime(request,id):
    tm = db.collection("tbl_time").document(id).get().to_dict()
    if request.method == "POST":
        data = {"time_name":request.POST.get("txt_time")}
        db.collection("tbl_time").document(id).update(data)
        return redirect("webadmin:time")
    else:
        return render(request,"Admin/Time.html",{"time":tm})

def day(request):
    day = db.collection("tbl_day").stream()
    day_data = []
    for i in day:
        data = i.to_dict()
        day_data.append({"day":data,"id":i.id})
    if request.method == "POST":
        data = {"day_name":request.POST.get("txt_day")}
        db.collection("tbl_day").add(data)
        return redirect("webadmin:day")
    else:
        return render(request,"Admin/Day.html",{"day":day_data})

def deleteday(request,id):
    db.collection("tbl_day").document(id).delete()
    return redirect("webadmin:day")

def updateday(request,id):
    day = db.collection("tbl_day").document(id).get().to_dict()
    if request.method == "POST":
        data = {"day_name":request.POST.get("txt_day")}
        db.collection("tbl_day").document(id).update(data)
        return redirect("webadmin:day")
    else:
        return render(request,"Admin/Day.html",{"days":day})
    