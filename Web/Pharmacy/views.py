from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import storage,auth,credentials,firestore
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

db = firestore.client()

def homepage(request):
    pharmacy = db.collection("tbl_pharmacy").document(request.session["pid"]).get().to_dict()
    return render(request,"Pharmacy/HomePage.html",{"pharmacy":pharmacy})

def profile(request):
    if 'pid' in request.session:
        pharmacy = db.collection("tbl_pharmacy").document(request.session["pid"]).get().to_dict()
        return render(request,"Pharmacy/Profile.html",{'pharmacy':pharmacy})
    else:
        return redirect("webguest:login")

def editprofile(request):
    if 'pid' in request.session:
        data = db.collection("tbl_pharmacy").document(request.session["pid"]).get().to_dict()
        if request.method == "POST":
            data = {'pharmacy_name':request.POST.get('txt_name'),'pharmacy_contact':request.POST.get('txt_contact'),'pharmacy_address':request.POST.get('txt_address')}
            db.collection("tbl_pharmacy").document(request.session["pid"]).update(data)
            return redirect("webpharmacy:profile")
        else:
            return render(request,"Pharmacy/EditProfile.html",{'pharmacy':data})
    else:
        return redirect("webguest:login")

def changepassword(request):
    pharmacy = db.collection("tbl_pharmacy").document(request.session["pid"]).get().to_dict()
    email = pharmacy["pharmacy_email"]
    pass_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
        'Reset your password ', 
        "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + pass_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Sync Medica.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    return render(request,"Pharmacy/Profile.html",{"msg":email})

def users(request):
    user_data = db.collection("tbl_user").stream()
    users = []
    for usersdata in user_data:
        users.append({"userdata":usersdata.to_dict(),"id":usersdata.id})  
    return render(request, "Pharmacy/Users.html", {'users': users})

def viewprescriptions(request,id):
    prescriptions = db.collection("tbl_prescription").where("user_id", "==", id).stream()
    pre_data = []
    for p in prescriptions:
        pre = p.to_dict()
        appointment = db.collection("tbl_appointments").document(pre["appointment_id"]).get().to_dict()
        con_details = db.collection("tbl_consultingdetails").document(appointment["consultingdetails_id"]).get().to_dict()
        cli_doc = db.collection("tbl_clinicdoctors").document(con_details["clinicdoctors_id"]).get().to_dict()
        doct = db.collection("tbl_doctor").document(cli_doc["doctor_id"]).get().to_dict()
        dept = db.collection("tbl_department").document(doct["doctor_department"]).get().to_dict()
        pre_data.append({"prescriptiondata":p.to_dict(),"id":p.id,"appointment":appointment,"doctor":doct,"doc_dept":dept})
    user_profile = db.collection("tbl_user").document(id).get().to_dict()
    return render(request, "Pharmacy/ViewPrescriptions.html", {'prescriptions': pre_data, 'user_profile': user_profile})

def ajaxsearch_patient(request):
    patient = db.collection("tbl_user").stream()
    p_data = []
    for p in patient:
        pt = p.to_dict()
        if pt["patient_id"].startswith(request.GET.get("pid")):
            p_data.append({"patientdata":p.to_dict()})
    return render(request,"Pharmacy/AjaxPatientSearch.html",{"patient":p_data})