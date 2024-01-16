from django.shortcuts import render
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

def userregistration(request):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for i in dis:
        data = i.to_dict()
        dis_data.append({"district":data,"id":i.id})
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            user = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Guest/UserRegistration.html",{"msg":error})

        image = request.FILES.get("txt_photo")
        if image:
            path = "User/Registration/" + image.name
            sd.child(path).put(image)
            download_url = sd.child(path).get_url(None)
        string = request.POST.get("txt_name") # Name text box 
        st = string.lower()
        data = st.split()
        res = ""
        for i in data:
        # print(i[0])
            res = res + i[0]
        # print(res)
        contact = request.POST.get("txt_contact") # Contact Text Box 
        # print(contact[6:10])
        # letter = data[0]
        val = "sm-"+res+contact[6:10]
        # print(val)

        user = {"patient_id":(val),
                "user_id":(user.uid),
                "user_photo":(download_url),
                "user_name":request.POST.get("txt_name"),
                "user_contact":request.POST.get("txt_contact"),
                "user_email":request.POST.get("txt_email"),
                "user_age":request.POST.get("txt_age"),
                "user_gender":request.POST.get("radio_gender"),
                "user_place":request.POST.get("sel_place"),
                "user_address":request.POST.get("txt_address"),}
        db.collection("tbl_user").add(user)
        return redirect("webguest:userregistration")
    else:
        return render(request,"Guest/UserRegistration.html",{"district":dis_data})
    
def pharmacyregistration(request):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for i in dis:
        data = i.to_dict()
        dis_data.append({"district":data,"id":i.id})
    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            pharmacy = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Guest/PharmacyRegistration.html",{"msg":error})

        image = request.FILES.get("txt_photo")
        if image:
            path = "Pharmacy/Registration/" + image.name
            sd.child(path).put(image)
            image_url = sd.child(path).get_url(None)
        
        certificateimage = request.FILES.get("txt_certificatephoto")
        if certificateimage:
            path = "Pharmacy/Certificate/" + certificateimage.name
            sd.child(path).put(certificateimage)
            certificate_url = sd.child(path).get_url(None)
        
        pharmacy = {"pharmacy_id":(pharmacy.uid),
                "pharmacy_photo":(image_url),
                "pharmacy_name":request.POST.get("txt_name"),
                "pharmacy_contact":request.POST.get("txt_contact"),
                "pharmacy_email":request.POST.get("txt_email"),
                "pharmacy_certificate":certificate_url,
                "pharmacy_place":request.POST.get("sel_place"),
                "pharmacy_address":request.POST.get("txt_address"),
                "pharmacy_status":"0"}
        db.collection("tbl_pharmacy").add(pharmacy)
        return redirect("webguest:pharmacyregistration")
    else:
        return render(request,"Guest/PharmacyRegistration.html",{"district":dis_data})
    
def doctorregistration(request):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for i in dis:
        data = i.to_dict()
        dis_data.append({"district":data,"id":i.id})

    dip = db.collection("tbl_department").stream()
    dip_data = []
    for i in dip:
        data = i.to_dict()
        dip_data.append({"department":data,"id":i.id})

    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            doctor = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Guest/DoctorRegistration.html",{"msg":error})

        image = request.FILES.get("txt_photo")
        if image:
            path = "Doctor/Registration/" + image.name
            sd.child(path).put(image)
            image_url = sd.child(path).get_url(None)
        
        idimage = request.FILES.get("txt_idphoto")
        if idimage:
            path = "Doctor/ID/" + idimage.name
            sd.child(path).put(idimage)
            id_url = sd.child(path).get_url(None)
        
        doctor = {"doctor_id":(doctor.uid),
                "doctor_photo":(image_url),
                "doctor_name":request.POST.get("txt_name"),
                "doctor_contact":request.POST.get("txt_contact"),
                "doctor_email":request.POST.get("txt_email"),
                "doctor_certificate":id_url,
                "doctor_place":request.POST.get("sel_place"),
                "doctor_department":request.POST.get("sel_department"),
                "doctor_address":request.POST.get("txt_address"),
                "doctor_qualification":request.POST.get("txt_qualification"),
                "doctor_about":request.POST.get("txt_about"),
                "doctor_status":"0"}
        db.collection("tbl_doctor").add(doctor)
        return redirect("webguest:doctorregistration")
    else:
        return render(request,"Guest/DoctorRegistration.html",{"district":dis_data,"department":dip_data})

def clinicregistration(request):
    dis = db.collection("tbl_district").stream()
    dis_data = []
    for i in dis:
        data = i.to_dict()
        dis_data.append({"district":data,"id":i.id})

    dip = db.collection("tbl_department").stream()
    dip_data = []
    for i in dip:
        data = i.to_dict()
        dip_data.append({"department":data,"id":i.id})

    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            clinic = firebase_admin.auth.create_user(email=email,password=password)
        except (firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Guest/ClinicRegistration.html",{"msg":error})

        image = request.FILES.get("txt_photo")
        if image:
            path = "Clinic/Registration/" + image.name
            sd.child(path).put(image)
            image_url = sd.child(path).get_url(None)
        
        certificateimage = request.FILES.get("txt_certificatephoto")
        if certificateimage:
            path = "Clinic/Certificate/" + certificateimage.name
            sd.child(path).put(certificateimage)
            certificate_url = sd.child(path).get_url(None)
        
        clinic = {"clinic_id":(clinic.uid),
                "clinic_photo":(image_url),
                "clinic_name":request.POST.get("txt_name"),
                "clinic_contact":request.POST.get("txt_contact"),
                "clinic_email":request.POST.get("txt_email"),
                "clinic_certificate":certificate_url,
                "clinic_place":request.POST.get("sel_place"),
                "clinic_address":request.POST.get("txt_address"),
                "clinic_status":"0"}
        db.collection("tbl_clinic").add(clinic)
        return redirect("webguest:clinicregistration")
    else:
        return render(request,"Guest/ClinicRegistration.html",{"district":dis_data})

def login(request):
    userid=""
    adminid=""
    clinicid=""
    pharmacyid=""
    doctorid=""
    medicalofficerid = medicalofficerdistrict = ""
    if request.method =="POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        try:
            data = authe.sign_in_with_email_and_password(email,password)
        except:
            return render(request,"Guest/Login.html",{"msg":"INVALID_LOGIN_CREDENTIALS... Check Email and Password"})
        id = data["localId"]
        user_data = db.collection("tbl_user").where("user_id", "==", id).stream()
        for u in user_data:
            userid = u.id
        admin_data = db.collection("tbl_admin").where("admin_id", "==", id).stream()
        for a in admin_data:
            adminid = a.id
        clinic_data = db.collection("tbl_clinic").where("clinic_id", "==", id).stream()
        for c in clinic_data:
            clinicid = c.id
        pharmacy_data = db.collection("tbl_pharmacy").where("pharmacy_id", "==", id).stream()
        for p in pharmacy_data:
            pharmacyid = p.id
        doctor_data = db.collection("tbl_doctor").where("doctor_id", "==", id).stream()
        for d in doctor_data:
            doctorid = d.id
        medicalofficer_data = db.collection("tbl_medicalofficer").where("medicalofficer_id", "==", id).stream()
        for m in medicalofficer_data:
            medicalofficerid = m.id
            data = m.to_dict()
            medicalofficerdistrict = data["medicalofficer_district"]
        if userid:
            request.session["uid"] = userid
            return redirect("webuser:homepage")
        elif adminid:
            request.session["aid"] = adminid
            return redirect("webadmin:homepage")
        elif clinicid:
            request.session["cid"] = clinicid
            return redirect("webclinic:homepage")
        elif pharmacyid:
            request.session["pid"] = pharmacyid
            return redirect("webpharmacy:homepage")
        elif doctorid:
            request.session["did"] = doctorid
            return redirect("webdoctor:homepage")
        elif medicalofficerid:
            request.session["mid"] = medicalofficerid
            request.session["med_district"] = medicalofficerdistrict
            return redirect("webmedicalofficer:homepage")
        else:
            return render(request,"Guest/Login.html",{"msg":"Error in Login"})
    else:
        return render(request,"Guest/Login.html")
    
def ajaxplace(request):
    place = db.collection("tbl_place").where("district_id", "==", request.GET.get("disd")).stream()
    place_data = []
    for p in place:
        place_data.append({"place":p.to_dict(),"id":p.id})
    return render(request,"Guest/AjaxPlace.html",{"place":place_data})
