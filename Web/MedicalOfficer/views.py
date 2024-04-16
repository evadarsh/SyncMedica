from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import storage,auth,credentials,firestore
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

db = firestore.client()

def homepage(request):
    if 'mid' in request.session:
        medicalofficer = db.collection("tbl_medicalofficer").document(request.session["mid"]).get().to_dict()
        return render(request,"Medicalofficer/HomePage.html",{"medicalofficer":medicalofficer})
    else:
        return redirect("webguest:login")
    
def error(request):
    return render(request,"Medicalofficer/404Error.html")

def logout(request):
    if 'mid' in request.session:
        request.session.pop("mid")
        return redirect("webguest:login")
    else:
        return redirect("webguest:login")
    
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
    
def accepteddoctorslist(request):
    if 'mid' in request.session:
        place = db.collection("tbl_place").where("district_id", "==", request.session["med_district"]).stream()
        doctor_data = []
        for p in place:
            doctor = db.collection("tbl_doctor").where("doctor_status", "==", "1").where("doctor_place", "==", p.id).stream()
            for s in doctor:
                doc = s.to_dict()
                dept = db.collection("tbl_department").document(doc["doctor_department"]).get().to_dict()
                doctor_data.append({"doctor":s.to_dict(),"id":s.id,"doc_dept":dept})
        return render(request,"MedicalOfficer/AcceptedDoctors.html",{"doctor":doctor_data})
    else:
        return render(request,"MedicalOfficer/HomePage.html")

def rejecteddoctorslist(request):
    if 'mid' in request.session:
        place = db.collection("tbl_place").where("district_id", "==", request.session["med_district"]).stream()
        doctor_data = []
        for p in place:
            doctor = db.collection("tbl_doctor").where("doctor_status", "==", "2").where("doctor_place", "==", p.id).stream()
            for s in doctor:
                doc = s.to_dict()
                dept = db.collection("tbl_department").document(doc["doctor_department"]).get().to_dict()
                doctor_data.append({"doctor":s.to_dict(),"id":s.id,"doc_dept":dept})
        return render(request,"MedicalOfficer/RejectedDoctors.html",{"doctor":doctor_data})
    else:
        return render(request,"MedicalOfficer/HomePage.html")

def acceptdoctor(request,id):
    data = {"doctor_status":"1"}
    db.collection("tbl_doctor").document(id).update(data)
    dname = db.collection("tbl_doctor").document(id).get().to_dict()["doctor_name"]
    email = db.collection("tbl_doctor").document(id).get().to_dict()["doctor_email"]
    send_mail(
                'Verification Successful',  
                "\rHello " + dname + ",\r\n\nWe have completed your document verifications and now you are eligible to use SyncMedica services.\r\n\nRegards.\r\nSync Medica.",  # Body
                settings.EMAIL_HOST_USER,
                [email],
                )
    return redirect("webmedicalofficer:accepteddoctorslist")

def rejectdoctor(request,id):
    data = {"doctor_status":"2"}
    db.collection("tbl_doctor").document(id).update(data)
    dname = db.collection("tbl_doctor").document(id).get().to_dict()["doctor_name"]
    email = db.collection("tbl_doctor").document(id).get().to_dict()["doctor_email"]
    send_mail(
                'Verification Rejected',  
                "\rHello " + dname + ",\r\n\nWe are unable to complete your document verifications due to some missing documents,You are requested to upload all relevent documents or visit the Medical Office for completing the document varifications to and enjoy SyncMedica services.\r\n\nRegards.\r\nSync Medica.",  # Body
                settings.EMAIL_HOST_USER,
                [email],
                )
    return redirect("webmedicalofficer:rejecteddoctorslist")

def approveclinic(request):
    if 'mid' in request.session:
        place = db.collection("tbl_place").where("district_id", "==", request.session["med_district"]).stream()
        clinic_data = []
        for p in place:
            clinic = db.collection("tbl_clinic").where("clinic_status", "==", "0").where("clinic_place", "==", p.id).stream()
            for s in clinic:
                clinic_data.append({"clinic":s.to_dict(),"id":s.id})
        return render(request,"MedicalOfficer/ApproveClinic.html",{"clinic":clinic_data})
    else:
        return render(request,"MedicalOfficer/HomePage.html")
    
def acceptedclinicslist(request):
    if 'mid' in request.session:
        place = db.collection("tbl_place").where("district_id", "==", request.session["med_district"]).stream()
        clinic_data = []
        for p in place:
            clinic = db.collection("tbl_clinic").where("clinic_status", "==", "1").where("clinic_place", "==", p.id).stream()
            for s in clinic:
                clinic_data.append({"clinic":s.to_dict(),"id":s.id})
        return render(request,"MedicalOfficer/AcceptedClinics.html",{"clinic":clinic_data})
    else:
        return render(request,"MedicalOfficer/HomePage.html")
    
def rejectedclinicslist(request):
    if 'mid' in request.session:
        place = db.collection("tbl_place").where("district_id", "==", request.session["med_district"]).stream()
        clinic_data = []
        for p in place:
            clinic = db.collection("tbl_clinic").where("clinic_status", "==", "2").where("clinic_place", "==", p.id).stream()
            for s in clinic:
                clinic_data.append({"clinic":s.to_dict(),"id":s.id})
        return render(request,"MedicalOfficer/RejectedClinics.html",{"clinic":clinic_data})
    else:
        return render(request,"MedicalOfficer/HomePage.html")

def acceptclinic(request,id):
    data = {"clinic_status":"1"}
    db.collection("tbl_clinic").document(id).update(data)
    cname = db.collection("tbl_clinic").document(id).get().to_dict()["clinic_name"]
    email = db.collection("tbl_clinic").document(id).get().to_dict()["clinic_email"]
    send_mail(
                'Verification Successful',  
                "\rHello " + cname + ",\r\n\nWe have completed your document verifications and now you are eligible to use SyncMedica services.\r\n\nRegards.\r\nSync Medica.",  # Body
                settings.EMAIL_HOST_USER,
                [email],
                )
    return redirect("webmedicalofficer:acceptedclinicslist")

def rejectclinic(request,id):
    data = {"clinic_status":"2"}
    db.collection("tbl_clinic").document(id).update(data)
    cname = db.collection("tbl_clinic").document(id).get().to_dict()["clinic_name"]
    email = db.collection("tbl_clinic").document(id).get().to_dict()["clinic_email"]
    send_mail(
                'Verification Rejected',  
                "\rHello " + cname + ",\r\n\nWe are unable to complete your document verifications due to some missing documents,You are requested to upload all relevent documents or visit the Medical Office for completing the document varifications to and enjoy SyncMedica services.\r\n\nRegards.\r\nSync Medica.",  # Body
                settings.EMAIL_HOST_USER,
                [email],
                )
    return redirect("webmedicalofficer:rejectedclinicslist")

def approvepharmacy(request):
    if 'mid' in request.session:
        place = db.collection("tbl_place").where("district_id", "==", request.session["med_district"]).stream()
        pharmacy_data = []
        for p in place:
            pharmacy = db.collection("tbl_pharmacy").where("pharmacy_status", "==", "0").where("pharmacy_place", "==", p.id).stream()
            for s in pharmacy:
                pharmacy_data.append({"pharmacy":s.to_dict(),"id":s.id})
        return render(request,"MedicalOfficer/ApprovePharmacy.html",{"pharmacy":pharmacy_data})
    else:
        return render(request,"MedicalOfficer/HomePage.html")
    
def acceptedpharmacieslist(request):
    if 'mid' in request.session:
        place = db.collection("tbl_place").where("district_id", "==", request.session["med_district"]).stream()
        pharmacy_data = []
        for p in place:
            pharmacy = db.collection("tbl_pharmacy").where("pharmacy_status", "==", "1").where("pharmacy_place", "==", p.id).stream()
            for s in pharmacy:
                pharmacy_data.append({"pharmacy":s.to_dict(),"id":s.id})
        return render(request,"MedicalOfficer/AcceptedPharmacies.html",{"pharmacy":pharmacy_data})
    else:
        return render(request,"MedicalOfficer/HomePage.html")
    
def rejectedpharmacieslist(request):
    if 'mid' in request.session:
        place = db.collection("tbl_place").where("district_id", "==", request.session["med_district"]).stream()
        pharmacy_data = []
        for p in place:
            pharmacy = db.collection("tbl_pharmacy").where("pharmacy_status", "==", "2").where("pharmacy_place", "==", p.id).stream()
            for s in pharmacy:
                pharmacy_data.append({"pharmacy":s.to_dict(),"id":s.id})
        return render(request,"MedicalOfficer/RejectedPharmacies.html",{"pharmacy":pharmacy_data})
    else:
        return render(request,"MedicalOfficer/HomePage.html")

    
def acceptpharmacy(request,id):
    data = {"pharmacy_status":"1"}
    db.collection("tbl_pharmacy").document(id).update(data)
    pname = db.collection("tbl_pharmacy").document(id).get().to_dict()["pharmacy_name"]
    email = db.collection("tbl_pharmacy").document(id).get().to_dict()["pharmacy_email"]
    send_mail(
                'Verification Successful',  
                "\rHello " + pname + ",\r\n\nWe have completed your document verifications and now you are eligible to use SyncMedica services.\r\n\nRegards.\r\nSync Medica.",  # Body
                settings.EMAIL_HOST_USER,
                [email],
                )
    return redirect("webmedicalofficer:acceptedpharmacieslist")

def rejectpharmacy(request,id):
    data = {"pharmacy_status":"2"}
    db.collection("tbl_pharmacy").document(id).update(data)
    pname = db.collection("tbl_pharmacy").document(id).get().to_dict()["pharmacy_name"]
    email = db.collection("tbl_pharmacy").document(id).get().to_dict()["pharmacy_email"]
    send_mail(
                'Verification Rejected',  
                "\rHello " + pname + ",\r\n\nWe are unable to complete your document verifications due to some missing documents,You are requested to upload all relevent documents or visit the Medical Office for completing the document varifications to and enjoy SyncMedica services.\r\n\nRegards.\r\nSync Medica.",  # Body
                settings.EMAIL_HOST_USER,
                [email],
                )
    return redirect("webmedicalofficer:rejectedpharmacieslist")

