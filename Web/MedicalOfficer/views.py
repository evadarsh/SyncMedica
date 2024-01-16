from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import storage,auth,credentials,firestore
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

db = firestore.client()

def homepage(request):
    medicalofficer = db.collection("tbl_medicalofficer").document(request.session["mid"]).get().to_dict()
    return render(request,"Medicalofficer/HomePage.html",{"medicalofficer":medicalofficer})

def profile(request):
    if 'mid' in request.session:
        medicalofficer = db.collection("tbl_medicalofficer").document(request.session["mid"]).get().to_dict()
        return render(request,"Medicalofficer/Profile.html",{'medicalofficer':medicalofficer})
    else:
        return redirect("webguest:login")

def editprofile(request):
    if 'mid' in request.session:
        data = db.collection("tbl_medicalofficer").document(request.session["mid"]).get().to_dict()
        if request.method == "POST":
            data = {'medicalofficer_name':request.POST.get('txt_name'),'medicalofficer_contact':request.POST.get('txt_contact')}
            db.collection("tbl_medicalofficer").document(request.session["mid"]).update(data)
            return redirect("webmedicalofficer:profile")
        else:
            return render(request,"Medicalofficer/EditProfile.html",{'medicalofficer':data})
    else:
        return redirect("webguest:login")

def changepassword(request):
    medicalofficer = db.collection("tbl_medicalofficer").document(request.session["mid"]).get().to_dict()
    email = medicalofficer["medicalofficer_email"]
    pass_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
        'Reset your password ',
        "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + pass_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Sync Medica.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    return render(request,"Medicalofficer/Profile.html",{"msg":email})


def approvedoctor(request):
    if 'mid' in request.session:
        place = db.collection("tbl_place").where("district_id", "==", request.session["med_district"]).stream()
        doctor_data = []
        for p in place:
            doctor = db.collection("tbl_doctor").where("doctor_status", "==", "0").where("doctor_place", "==", p.id).stream()
            for s in doctor:
                doc = s.to_dict()
                dept = db.collection("tbl_department").document(doc["doctor_department"]).get().to_dict()
                doctor_data.append({"doctor":s.to_dict(),"id":s.id,"doc_dept":dept})
        return render(request,"MedicalOfficer/ApproveDoctor.html",{"doctor":doctor_data})
    else:
        return render(request,"MedicalOfficer/HomePage.html")
    
def acceptdoctor(request,id):
    data = {"doctor_status":"1"}
    db.collection("tbl_doctor").document(id).update(data)
    return redirect("webmedicalofficer:approvedoctor")

def rejecttdoctor(request,id):
    data = {"doctor_status":"1"}
    db.collection("tbl_doctor").document(id).update(data)
    return redirect("webmedicalofficer:approvedoctor")

