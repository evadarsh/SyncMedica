from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import storage,auth,credentials,firestore
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

db = firestore.client()

def homepage(request):
    medicalofficer = db.collection("tbl_medicalofficer").document(request.session["uid"]).get().to_dict()
    return render(request,"medicalofficer/HomePage.html",{"medicalofficer":medicalofficer})

def profile(request):
    if 'uid' in request.session:
        medicalofficer = db.collection("tbl_medicalofficer").document(request.session["uid"]).get().to_dict()
        return render(request,"medicalofficer/Profile.html",{'medicalofficer':medicalofficer})
    else:
        return redirect("webguest:login")

def editprofile(request):
    if 'uid' in request.session:
        data = db.collection("tbl_medicalofficer").document(request.session["uid"]).get().to_dict()
        if request.method == "POST":
            data = {'medicalofficer_name':request.POST.get('txt_name'),'medicalofficer_contact':request.POST.get('txt_contact'),'medicalofficer_address':request.POST.get('txt_address')}
            db.collection("tbl_medicalofficer").document(request.session["uid"]).update(data)
            return redirect("webmedicalofficer:profile")
        else:
            return render(request,"medicalofficer/EditProfile.html",{'medicalofficer':data})
    else:
        return redirect("webguest:login")

def changepassword(request):
    medicalofficer = db.collection("tbl_medicalofficer").document(request.session["uid"]).get().to_dict()
    email = medicalofficer["medicalofficer_email"]
    pass_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
        'Reset your password ', #subject
        "\rHello \r\nFollow this link to reset your Project password for your " + email + "\n" + pass_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
        settings.EMAIL_HOST_USER,
        [email],
    )
    return render(request,"medicalofficer/Profile.html",{"msg":email})