from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import storage,auth,credentials,firestore
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

db = firestore.client()

def homepage(request):
    clinic = db.collection("tbl_clinic").document(request.session["cid"]).get().to_dict()
    return render(request,"Clinic/HomePage.html",{"clinic":clinic})

def profile(request):
    if 'cid' in request.session:
        clinic = db.collection("tbl_clinic").document(request.session["cid"]).get().to_dict()
        return render(request,"Clinic/Profile.html",{'clinic':clinic})
    else:
        return redirect("webguest:login")

def editprofile(request):
    if 'cid' in request.session:
        data = db.collection("tbl_clinic").document(request.session["cid"]).get().to_dict()
        if request.method == "POST":
            data = {'clinic_name':request.POST.get('txt_name'),'clinic_contact':request.POST.get('txt_contact'),'clinic_address':request.POST.get('txt_address')}
            db.collection("tbl_clinic").document(request.session["cid"]).update(data)
            return redirect("webclinic:profile")
        else:
            return render(request,"Clinic/EditProfile.html",{'clinic':data})
    else:
        return redirect("webguest:login")

def changepassword(request):
    clinic = db.collection("tbl_clinic").document(request.session["cid"]).get().to_dict()
    email = clinic["clinic_email"]
    pass_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
        'Reset your password ', #subject
        "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + pass_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Sync Medica.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    return render(request,"Clinic/Profile.html",{"msg":email})


def notification(request):
    notification = db.collection("tbl_clinic").where("clinic_id", "==", request.GET.get("cid")).stream()
    notification_data = []
    for i in notification:
        data = i.to_dict()
        notification_data.append({"notification":data,"id":i.id})
    if request.method == "POST":
        data = {"notification_title":request.POST.get("txt_notificationtitle"),"notification_details":request.POST.get("txt_notificationdetails"),"clinic_id":request.session["cid"]}
        db.collection("tbl_notification").add(data)
        return redirect("webclinic:notification")
    else:
        return render(request,"Clinic/Notification.html",{"notification":notification_data})

def clinicdoctors(request):
    doctor = db.collection("tbl_doctor").where("doctor_status", "==", "1").stream()
    doctor_data = []
    for d in doctor:
        doctor_data.append({"doctor":d.to_dict(),"id":d.id})

    clinicdoctors = db.collection("tbl_clinicdoctors").where("clinic_id", "==", request.session["cid"]).stream()
    clinicdoctors_data = []
    for c in clinicdoctors:
        data = c.to_dict()
        doc = db.collection("tbl_doctor").document(data["doctor_id"]).get().to_dict()
        clinicdoctors_data.append({"clinicdoctors":data,"id":c.id,"doctor":doc})

    if request.method == "POST":
        data = {"doctor_id":request.POST.get("sel_doctor"),"clinic_id":request.session["cid"],"doctor_status":"0"}
        db.collection("tbl_clinicdoctors").add(data)
        return redirect("webclinic:clinicdoctors")
    else:
        return render(request,"Clinic/ClinicDoctors.html",{"clinicdoctors":clinicdoctors_data,"doctor":doctor_data})

def deletedoctor(request,id):
    db.collection("tbl_clinicdoctors").document(id).delete()
    consultingdetails_data = db.collection("tbl_consultingdetails").where("clinicdoctors_id", "==", id).stream()
    for i in consultingdetails_data:
        db.collection("tbl_consultingdetails").document(i.id).delete()
    return redirect("webclinic:clinicdoctors")

def consultingdetails(request,id):
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
    if request.method == "POST":
        data = {"clinicdoctors_id":id,"time_id":request.POST.get("sel_time"),"day_id":request.POST.get("sel_day"),"consulting_fee":request.POST.get("txt_fee"),"doctor_token":request.POST.get("txt_token"),"clinicdetails_status":"0"}
        db.collection("tbl_consultingdetails").add(data)
        db.collection("tbl_clinicdoctors").document(id).update({"doctor_status":"3"})
        return redirect("webclinic:clinicdoctors")
    else:
        return render(request,"Clinic/ConsultingDetails.html",{"consultingdetails":cdata,"time":tdata,"day":ddata})

def deleteconsultingdetails(request,id):
    db.collection("tbl_consultingdetails").document(id).delete()
    return redirect("webclinic:clinicdoctors")

def updateconsultingdetails(request,id):
    time_data = db.collection("tbl_time").stream()
    tdata = []
    for t in time_data:
        tdata.append({"time":t.to_dict(),"id":t.id})
    day_data = db.collection("tbl_day").stream()
    ddata = []
    for d in day_data:
        ddata.append({"day":d.to_dict(),"id":d.id})
    consultingdetails_data = db.collection("tbl_consultingdetails").document(id).get().to_dict()
    if request.method == "POST":
        data = {"time_id":request.POST.get("sel_time"),"day_id":request.POST.get("sel_day"),"consulting_fee":request.POST.get("txt_fee"),"doctor_token":request.POST.get("txt_token")}
        db.collection("tbl_consultingdetails").document(id).update(data)
        return redirect("webclinic:clinicdoctors")
    else:
        return render(request,"Clinic/ConsultingDetails.html",{"consultingdata":consultingdetails_data,"time":tdata,"day":ddata})