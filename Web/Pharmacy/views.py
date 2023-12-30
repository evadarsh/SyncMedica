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
        'Reset your password ', #subject
        "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + pass_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    return render(request,"Pharmacy/Profile.html",{"msg":email})