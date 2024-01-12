from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import storage,auth,credentials,firestore
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import date
from django.utils import timezone
import pytz

db = firestore.client()

def homepage(request):
    # Get the current time in UTC
    current_time_utc = timezone.now()
    print(current_time_utc)

    # Get the Indian time zone
    indian_timezone = pytz.timezone('Asia/Kolkata')

    # Convert the current time to the Indian time zone
    current_time_indian = current_time_utc.astimezone(indian_timezone)

    # Print the current time in the Indian time zone
    print("Current Time (Indian):", current_time_indian)
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    return render(request,"User/HomePage.html",{"user":user})

def profile(request):
    if 'uid' in request.session:
        user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
        return render(request,"User/Profile.html",{'user':user})
    else:
        return redirect("webguest:login")

def editprofile(request):
    if 'uid' in request.session:
        data = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
        if request.method == "POST":
            data = {'user_name':request.POST.get('txt_name'),'user_contact':request.POST.get('txt_contact'),'user_address':request.POST.get('txt_address')}
            db.collection("tbl_user").document(request.session["uid"]).update(data)
            return redirect("webuser:profile")
        else:
            return render(request,"User/EditProfile.html",{'user':data})
    else:
        return redirect("webguest:login")

def changepassword(request):
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    email = user["user_email"]
    pass_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
        'Reset your password ', #subject
        "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + pass_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Sync Medica.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    return render(request,"User/Profile.html",{"msg":email})

def searchclinic(request):
    if 'uid' in request.session:
        district = db.collection("tbl_district").stream()
        dis_data = []
        for i in district:
            dis_data.append({"district":i.to_dict(),"id":i.id})
        if request.method == "POST":
            clinic = db.collection("tbl_clinic").where("clinic_place", "==", request.POST.get("sel_place")).stream()
            clinic_data = []
            for s in clinic:
                clinic_data.append({"clinic":s.to_dict(),"id":s.id})
            return render(request,"User/SearchClinic.html",{"dis":dis_data,"clinic":clinic_data})
        else:
            return render(request,"User/SearchClinic.html",{"dis":dis_data})
    else:
        return redirect("webguest:login")

def viewdoctors(request,id):
    if 'uid' in request.session:
        clinicdoctors = db.collection("tbl_clinicdoctors").where("clinic_id", "==",id).where("doctor_status", ">=","3").stream()
        doctors_data = []
        for i in clinicdoctors:
            clinicdoctors_data = i.to_dict()
            doctor_data = db.collection("tbl_doctor").document(clinicdoctors_data["doctor_id"]).get().to_dict()
            doctors_data.append({"doctor":doctor_data,"clinic":clinicdoctors_data,"id":i.id})
        return render(request,"User/ViewDoctors.html",{"doctor":doctors_data})
    else:
        return redirect("webguest:login")

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
    if request.method == "POST":
        datedata = date.today()
        data = {"consultingdetails_id":request.POST.get("sel_time"),"appointment_date":request.POST.get("txt_date"),"user_id":(request.session["uid"]),"booking_date":str(datedata),"appointment_status":"0"}
        db.collection("tbl_appointments").add(data)
        return redirect("webuser:homepage")
    else:
        return render(request,"User/ViewDetails.html",{"consultingdetails":cdata})

def ajaxclinic(request):
    clinic_data = []
    if request.GET.get("pid") != "":
        clinic = db.collection("tbl_clinic").where("place_id", "==", request.GET.get("pid")).stream()
        for i in clinic:
            clinic_data.append({"clinic":i.to_dict(),"id":i.id})
    else:
        place = db.collection("tbl_place").where("district_id", "==", request.GET.get("did")).stream()
        for p in place:
            clinic = db.collection("tbl_clinic").where("place_id", "==", p.id).stream()
            for i in clinic:
                clinic_data.append({"clinic":i.to_dict(),"id":i.id})
    return render(request,"User/AjaxClinic.html",{"clinic":clinic_data})

def ajaxplace(request):
    place = db.collection("tbl_place").where("district_id", "==", request.GET.get("disd")).stream()
    place_data = []
    for p in place:
        place_data.append({"place":p.to_dict(),"id":p.id})
    return render(request,"Guest/AjaxPlace.html",{"place":place_data})

def ajaxbooking(request):
    if request.GET.get("date") != "":
        bookings = db.collection("tbl_appointments").where("consultingdetails_id", "==", request.GET.get("conid")).where("appointment_date", "==", request.GET.get("date")).where("appointment_status", "==", "0").stream()
        book = []
        for b in bookings:
            bdata = b.to_dict()
            doc_details = db.collection("tbl_consultingdetails").document(bdata["consultingdetails_id"]).get().to_dict()
            book.append({"book":bdata,"con_details":doc_details})
        token = db.collection("tbl_consultingdetails").document(request.GET.get("conid")).get().to_dict()
        if int(token["doctor_token"]) > len(book):
            return render(request,"User/AjaxBooking.html",{"msg":""})
        else:
            return render(request,"User/AjaxBooking.html",{"msg":"No Enough Tokens To Book"})
    else:
        return render(request,"User/ViewDetails.html")