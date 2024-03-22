from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import storage,auth,credentials,firestore
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import random
from datetime import datetime
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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

def checkstatus(request,id):
    user=db.collection("tbl_user").document(id).get().to_dict()
    email = user["user_email"]
    if user["user_status"] == "0":
        return redirect("webpharmacy:viewprescriptions",id=id)
    else:
        otp = random.randint(100000,999999)
        # print(otp)
        request.session["otp"] = otp
        send_mail(
            'OPEN YOUR ACCOUNT ', 
            "\rHello \r\n Your One Time Password(OTP) for login is " + str(otp) + ".\n If you didn't ask to open your account, you can ignore this email. \r\n Thanks. \r\n Sync Medica.",#body
            settings.EMAIL_HOST_USER,
            [email],
        )
        return redirect("webpharmacy:otpverification",id=id)

def viewprescriptions(request,id):
    prescriptions = db.collection("tbl_prescription").order_by("prescription_date", direction=firestore.Query.DESCENDING).where("user_id", "==", id).stream()
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

def generatebill(request,id):
    bill = db.collection("tbl_bill").where("pharmarcy_id", "==", request.session["pid"]).where("prescription_id", "==", id).where("status", "==", 0).order_by("time", direction=firestore.Query.DESCENDING).stream()
    bill_data = []
    total = 0
    for b in bill:
        bi = b.to_dict()
        total = total + int(bi["qty"]) * int(bi["rate"])
        bill_data.append({"bills":b.to_dict(),"id":b.id})        
    # print(total)
    count = db.collection("tbl_bill").where("pharmarcy_id", "==", request.session["pid"]).where("prescription_id", "==", id).where("status", "==", 1).get()
    # print(len(count))
    return render(request,"Pharmacy/GenerateBill.html",{"bill":bill_data,"id":id,"total":total,"count":len(count)})

def ajaxaddbill(request):
    db.collection("tbl_bill").add({"Name":request.GET.get("name"),"qty":request.GET.get("qty"),"rate":request.GET.get("rate"),"pharmarcy_id":request.session["pid"],"prescription_id":request.GET.get("pre"),"status":0,"time":datetime.now()})
    ajaxbill = db.collection("tbl_bill").where("pharmarcy_id", "==", request.session["pid"]).where("prescription_id", "==", request.GET.get("pre")).where("status", "==", 0).order_by("time", direction=firestore.Query.DESCENDING).stream()
    bl_datas = []
    total = 0
    for bill in ajaxbill:
        bi = bill.to_dict()
        total = total + int(bi["qty"]) * int(bi["rate"])
        bl_datas.append({"billdata":bill.to_dict(),"id":bill.id})
    # print(bl_datas)
    count = db.collection("tbl_bill").where("pharmarcy_id", "==", request.session["pid"]).where("prescription_id", "==", request.GET.get("pre")).where("status", "==", 1).get()
    return render(request,"Pharmacy/AjaxAddBill.html",{"bill":bl_datas,"total":total,"count":len(count)})

def ajaxdeletebill(request):
    db.collection("tbl_bill").document(request.GET.get("id")).delete()
    ajaxbill = db.collection("tbl_bill").where("pharmarcy_id", "==", request.session["pid"]).where("prescription_id", "==", request.GET.get("pre")).where("status", "==", 0).order_by("time", direction=firestore.Query.DESCENDING).stream()
    bl_datas = []
    total = 0
    for bill in ajaxbill:
        bi = bill.to_dict()
        total = total + int(bi["qty"]) * int(bi["rate"])
        bl_datas.append({"billdata":bill.to_dict(),"id":bill.id})
    count = db.collection("tbl_bill").where("pharmarcy_id", "==", request.session["pid"]).where("prescription_id", "==", request.GET.get("pre")).where("status", "==", 1).get()
    return render(request,"Pharmacy/AjaxAddBill.html",{"bill":bl_datas,"total":total,"count":len(count)})

def checkqty(request):
    db.collection("tbl_bill").document(request.GET.get("id")).update({"qty":request.GET.get("qty")})
    ajaxbill = db.collection("tbl_bill").where("pharmarcy_id", "==", request.session["pid"]).where("prescription_id", "==", request.GET.get("pre")).where("status", "==", 0).order_by("time", direction=firestore.Query.DESCENDING).stream()
    bl_datas = []
    total = 0
    for bill in ajaxbill:
        bi = bill.to_dict()
        total = total + int(bi["qty"]) * int(bi["rate"])
        bl_datas.append({"billdata":bill.to_dict(),"id":bill.id})
    count = db.collection("tbl_bill").where("pharmarcy_id", "==", request.session["pid"]).where("prescription_id", "==", request.GET.get("pre")).where("status", "==", 1).get()
    return render(request,"Pharmacy/AjaxAddBill.html",{"bill":bl_datas,"total":total,"count":len(count)})

def ajaxsubmitbill(request):
    bills = db.collection("tbl_bill").where("pharmarcy_id", "==", request.session["pid"]).where("prescription_id", "==", request.GET.get("pre")).where("status", "==", 0).stream()
    for b in bills:
        db.collection("tbl_bill").document(b.id).update({"status":1})
    return JsonResponse({"msg":"Bill Generated Successfully"})

def viewbills(request,id):
    ajaxbill = db.collection("tbl_bill").where("pharmarcy_id", "==", request.session["pid"]).where("prescription_id", "==", id).where("status", "==", 1).order_by("time", direction=firestore.Query.DESCENDING).stream()
    bl_datas = []
    total = 0
    date = ""
    phar = ""
    for bill in ajaxbill:
        bi = bill.to_dict()
        date = bi["time"]
        total = total + int(bi["qty"]) * int(bi["rate"])
        pharmacy = db.collection("tbl_pharmacy").document(bi["pharmarcy_id"]).get().to_dict()
        bl_datas.append({"billdata":bill.to_dict(),"id":bill.id,"pharmacy":pharmacy})
    user = getuser(id)
    email = user["user_email"]
    ran = random.randint(100000,999999)
    return render(request,"Pharmacy/View_Bill.html",{"bill":bl_datas,"total":total,"user":user,"date":date,"ran":ran,"phar":pharmacy})

def getuser(id):
    pre = db.collection("tbl_prescription").document(id).get().to_dict()
    user = db.collection("tbl_user").document(pre["user_id"]).get().to_dict()
    # print(user)
    return user

def otpverification(request,id):
    if request.method == "POST":
        otp = request.session["otp"]
        text = int(request.POST.get("txt_otp"))
        if text == otp:
            print("hai")
            del request.session["otp"]
            return redirect("webpharmacy:viewprescriptions",id=id)
        else:
            return render(request,"Pharmacy/OTP.html",{"msg":"Invalid OTP"})
    else:
        return render(request,"Pharmacy/OTP.html")

def ajaxsearch_patient(request):
    patient = db.collection("tbl_user").stream()
    p_data = []
    for p in patient:
        pt = p.to_dict()
        if pt["patient_id"].startswith(request.GET.get("pid")):
            p_data.append({"patientdata":p.to_dict(),"id":p.id})
    return render(request,"Pharmacy/AjaxPatientSearch.html",{"patient":p_data})