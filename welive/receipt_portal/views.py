from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from docxtpl import DocxTemplate
import pandas as pd
import os
import glob
import smtplib
from email.mime.text import MIMEText

# Create your views here.
def say_hello(request):
    return render(request,'hello.html',{'Name':'Rithvik'})

def home(request):
    if not request.user.is_authenticated: #if the user is not authenticated
        return HttpResponseRedirect(reverse("login")) #redirect to login page
    else:
        directory = settings.MEDIA_ROOT + "/"
        files = glob.glob(settings.MEDIA_ROOT+"/*")
        options = [file.replace(directory, '') for file in files if os.path.isfile(file)]

        return render(request,'main/home.html', {
                'uploaded_files': options
            })

def generate_receipt(request):
    #Logic for generating the docx file
    file = request.POST.get("selected_file")
    #Add error checking for format and save files in a different directory
    values = pd.read_excel("media/" + file)
    slot_no = values["S No"]
    names = values["Name of the Donor"]
    amount = values["Donation Amount	"]
    address = values["Address"]
    date = values["Donation Date"]
    pan = values["PAN No."]
    #Create receipt directory if needed
    #Change logic for serial number
    receipts = len(slot_no)
    doc = DocxTemplate("/home/rithvik/WeLive/welive/media/format/Receipt_Format-4.docx")
    for i in range(receipts):
        context = { 'donar_name' : names[i],
                    'donor_address': address[i],
                    'donor_pan': pan[i],
                    'donation_amount': amount[i],
                    'date': date[i],
                    'receipt_no': slot_no[i]}
        doc.render(context)
        final_path = "media/receipts/" + str(slot_no[i]) + "_receipt.docx"
        doc.save(final_path)
        #Check os and then use one or the other
        os.system("lowriter --convert-to pdf" +str(" ") + str(final_path))
        os.system("rm " + str(final_path))
    os.system("mv *.pdf media/receipts")
    return HttpResponseRedirect(reverse("home"))

def upload_file(request):
    #Logic for uploading files
    #Create format directoy if needed
    myfile = request.FILES['myfile']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    return HttpResponseRedirect(reverse("home"))

def send_email(request):
    subject = "Email Subject"
    body = "This is the body of the text message"
    sender = "rithvik.ravilla@gmail.com"
    recipients = ["rithvik.ravilla@gmail.com"]
    password = "rkxr vgfs eecb yxyz"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())