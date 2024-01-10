from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from receipt_portal.models import Email
from docxtpl import DocxTemplate
import pandas as pd
import os
import glob
import smtplib
import shutil
from docx2pdf import convert
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import pythoncom


# Create your views here.
def say_hello(request):
    return render(request,'hello.html',{'Name':'Rithvik'})

def home(request):
    if not request.user.is_authenticated: #if the user is not authenticated
        return HttpResponseRedirect(reverse("login")) #redirect to login page
    else:
        
        directory = settings.MEDIA_ROOT + "\\"
        files = glob.glob(settings.MEDIA_ROOT+"\*")
        file_options = [file.replace(directory, '') for file in files if os.path.isfile(file)]
        
        receipt_dir = os.path.join(settings.MEDIA_ROOT,"pdf\\")
        receipts = glob.glob(os.path.join(settings.MEDIA_ROOT,"pdf\*"))
        directory_options = [receipt.replace(receipt_dir, '') for receipt in receipts if os.path.isdir(receipt)]
        
        return render(request,'main/home.html', {
                'uploaded_files': file_options,
                'receipts': directory_options
            })

def generate_receipt(request):
    file = request.POST.get("selected_file")
    stripped_file = os.path.splitext(file)[0]
    input_directory = os.path.join(settings.MEDIA_ROOT, "word_docs", str(stripped_file))
    os.makedirs(input_directory, exist_ok=True)
    
    #Add error checking for uploaded file format
    file_path = os.path.join(settings.MEDIA_ROOT,file)
    values = pd.read_excel(file_path)
    slot_no = values["S No"]
    
    doc = DocxTemplate(os.path.join(settings.MEDIA_ROOT,"format","Receipt_Format-4.docx"))
    for i in range(len(slot_no)):
        context = { 'donar_name' : values["Name of the Donor"][i],
                    'donor_address': values["Address"][i],
                    'donor_pan': values["PAN No."][i],
                    'donation_amount': values["Donation Amount	"][i],
                    'date': values["Donation Date"][i],
                    'receipt_no': slot_no[i]}
        doc.render(context)
        final_path=  os.path.join(settings.MEDIA_ROOT,"word_docs",stripped_file,str(slot_no[i]) + "_receipt.docx")
        doc.save(final_path)

    #Using microsoft word specific docx2pdf lib
    output_dir = os.path.join(settings.MEDIA_ROOT, "pdf", str(stripped_file))
    os.makedirs(output_dir, exist_ok=True)
    #pythoncom to give python access to word
    pythoncom.CoInitialize()
    convert(input_directory,output_dir)
    return HttpResponseRedirect(reverse("home"))

def delete_receipt(request):
    file = request.POST.get("selected_file")
    stripped_file = os.path.splitext(file)[0]
    shutil.rmtree("media/" + "receipts/" + stripped_file)

def upload_file(request):
    #Make a delete file button and option
    #Create format directory to upload the template
    myfile = request.FILES['myfile']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    return HttpResponseRedirect(reverse("home"))

def send_email(request):
    dir = request.POST.get("selected_directory")
    
    values = pd.read_excel(os.path.join(settings.MEDIA_ROOT, dir + ".xlsx"))
    slot_no = values["S No"]
    emails = values["Email Address"]

    #Email details from sqlite
    email_details = Email.objects.all() 
    body = MIMEText(email_details[0].body) # convert the body to a MIME compatible string
    subject = email_details[0].subject
    sender = email_details[0].sender
    password = email_details[0].app_password
    
    for i in range(len(slot_no)):
        msg = MIMEMultipart()
        msg.attach(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = emails[i]
        pdf = os.path.join(settings.MEDIA_ROOT,"pdf",dir,str(slot_no[i]) + "_receipt.pdf")
        with open(pdf, "rb") as pdf_file:
            pdf_attachment = MIMEApplication(pdf_file.read())
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename= str(slot_no[i]) + "_receipt.pdf")
            msg.attach(pdf_attachment)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, emails[i], msg.as_string())
    
    return HttpResponseRedirect(reverse("home"))
    