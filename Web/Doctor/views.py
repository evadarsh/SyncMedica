from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import storage,auth,credentials,firestore
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

db = firestore.client()

def homepage(request):
    doctor = db.collection("tbl_doctor").document(request.session["did"]).get().to_dict()
    return render(request,"Doctor/HomePage.html",{"doctor":doctor})

def logout(request):
    if 'did' in request.session:
        request.session.pop("did")
        return redirect("webguest:login")
    else:
        return redirect("webguest:login")

def profile(request):
    if 'did' in request.session:
        doctor = db.collection("tbl_doctor").document(request.session["did"]).get().to_dict()
        return render(request,"Doctor/Profile.html",{'doctor':doctor})
    else:
        return redirect("webguest:login")

def editprofile(request):
    dip = db.collection("tbl_department").stream()
    dip_data = []
    for i in dip:
        data = i.to_dict()
        dip_data.append({"department":data,"id":i.id})
    
    if 'did' in request.session:
        data = db.collection("tbl_doctor").document(request.session["did"]).get().to_dict()
        if request.method == "POST":
            data = {'doctor_name':request.POST.get('txt_name'),'doctor_contact':request.POST.get('txt_contact'),'doctor_address':request.POST.get('txt_address'),"doctor_qualification":request.POST.get("txt_qualification"),"doctor_about":request.POST.get("txt_about"),"doctor_department":request.POST.get("sel_department"),"doctor_place":request.POST.get("sel_place")}
            db.collection("tbl_doctor").document(request.session["did"]).update(data)
            return redirect("webdoctor:profile")
        else:
            return render(request,"Doctor/EditProfile.html",{'doctor':data,'department':dip_data})
    else:
        return redirect("webguest:login")

def changepassword(request):
    doctor = db.collection("tbl_doctor").document(request.session["did"]).get().to_dict()
    email = doctor["doctor_email"]
    pass_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
        'Reset your password ', #subject
        "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + pass_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Sync Medica.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    return render(request,"Doctor/Profile.html",{"msg":email})

def clinicrequests(request):
    clinic = db.collection("tbl_clinic").stream()
    clinic_data = []
    for d in clinic:
        clinic_data.append({"clinic":d.to_dict(),"id":d.id})

    clinicdoctors = db.collection("tbl_clinicdoctors").where("doctor_status", "==", "0").where("doctor_id", "==", request.session["did"]).stream()
    clinicdoctors_data = []
    for c in clinicdoctors:
        data = c.to_dict()
        clinic = db.collection("tbl_clinic").document(data["clinic_id"]).get().to_dict()
        clinicdoctors_data.append({"clinicdoctors": data, "id": c.id,"clinic":clinic})
    if request.method == "POST":
        data = {"doctor_id": request.POST.get("sel_doctor"), "clinic_id": request.session["cid"], "doctor_status": "0"}
        db.collection("tbl_clinicdoctors").add(data)
        return redirect("webdoctor:clinicrequests")
    else:
        return render(request, "Doctor/ClinicRequests.html", {"clinicdoctors": clinicdoctors_data})

    
def updateclinic(request, id):
    data = {"doctor_status": "2"}
    db.collection("tbl_clinicdoctors").document(id).update(data)
    return render(request,"Doctor/ClinicRequests.html",{"msg":"Request Approved..."})

def rejectclinic(request, id):
    data = {"doctor_status": "1"}
    db.collection("tbl_clinicdoctors").document(id).update(data)
    return render(request,"Doctor/ClinicRequests.html",{"msg":"Request Rejected..."})

def consultingdeatils(request):
    clinic = db.collection("tbl_clinic").stream()
    clinic_data = []
    for d in clinic:
        clinic_data.append({"clinic":d.to_dict(),"id":d.id})

    clinicdoctors = db.collection("tbl_clinicdoctors").where("doctor_status", ">=", "2").where("doctor_id", "==", request.session["did"]).stream()
    clinicdoctors_data = []
    for c in clinicdoctors:
        data = c.to_dict()
        clinic = db.collection("tbl_clinic").document(data["clinic_id"]).get().to_dict()
        clinicdoctors_data.append({"clinicdoctors": data, "id": c.id,"clinic":clinic})
    if request.method == "POST":
        data = {"doctor_id": request.POST.get("sel_doctor"), "clinic_id": request.session["cid"], "doctor_status": "0"}
        db.collection("tbl_clinicdoctors").add(data)
        return redirect("webdoctor:consultingdetails")
    else:
        return render(request, "Doctor/ConsultingDetails.html", {"clinicdoctors": clinicdoctors_data})
    
def viewdetails(request,id):
    time_data = db.collection("tbl_time").stream()
    tdata = []
    for t in time_data:
        tdata.append({"time":t.to_dict(),"id":t.id})
    day_data = db.collection("tbl_day").stream()
    ddata = []
    for d in day_data:
        ddata.append({"day":d.to_dict(),"id":d.id})
    consultingdetails_data = db.collection("tbl_consultingdetails").where("clinicdoctors_id", "==", id).stream()
    cdata = []
    for c in consultingdetails_data:
        data = c.to_dict()
        time = db.collection("tbl_time").document(data["time_id"]).get().to_dict()
        day = db.collection("tbl_day").document(data["day_id"]).get().to_dict()
        cdata.append({"consultingdata":c.to_dict(),"id":c.id,"timedata":time,"daydata":day}) 
    return render(request,"Doctor/ViewDetails.html",{"consultingdetails":cdata})
    
def appointments(request,id):
    appointments = db.collection("tbl_appointments").where("appointment_status", "==", "0").where("consultingdetails_id", "==", id).stream()
    appointment_data =[]
    for a in appointments:
        appointments_data = a.to_dict()
        user = db.collection("tbl_user").document(appointments_data["user_id"]).get().to_dict()
        appointment_data.append({"appointmentdetails":a.to_dict(),"id":a.id,"user":user}) 
    return render(request,"Doctor/ViewAppointments.html",{"appointments":appointment_data})

def prescription(request,id):
    appointments = db.collection("tbl_appointments").document(id).get().to_dict()
    userdata = db.collection("tbl_user").document(appointments["user_id"]).get().to_dict()
    if request.method == "POST":
        data = {"user_id":appointments["user_id"],"appointment_id": id,"prescription":request.POST.get("txt_prescription"),"description":request.POST.get("txt_description"),"prescription_status": "0","prescription_date":appointments["appointment_date"] }
        db.collection("tbl_prescription").add(data)
        status = {"appointment_status": "1"}
        db.collection("tbl_appointments").document(id).update(status)
        return redirect("webdoctor:homepage")
    return render(request,"Doctor/AddPrescription.html",{"user":userdata})