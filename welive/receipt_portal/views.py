from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
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
import sys


# Used for testing values.
def say_hello(request):
    return render(request,'hello.html',{'Name':'Rithvik'})

def home(request):
    if not request.user.is_authenticated: #if the user is not authenticated
        return HttpResponseRedirect(reverse("login")) #redirect to login page
    else:
        #Keeping the receipt dir and uploaded option as context
        directory = os.path.join(settings.MEDIA_ROOT,"upload\\")
        files = glob.glob(os.path.join(settings.MEDIA_ROOT,"upload\*"))
        file_options = [file.replace(directory, '') for file in files if os.path.isfile(file)]

        receipt_dir = os.path.join(settings.MEDIA_ROOT,"pdf\\")
        receipts = glob.glob(os.path.join(settings.MEDIA_ROOT,"pdf\*"))
        directory_options = [receipt.replace(receipt_dir, '') for receipt in receipts if os.path.isdir(receipt)]
        
        return render(request,'main/home.html', {
                'uploaded_files': file_options,
                'receipts': directory_options
            })

def generate_receipt(request,file):
    try:
        #Removing the extension and checking if pdf and word_doc directory exists
        stripped_file = os.path.splitext(file)[0]
        input_directory = os.path.join(settings.MEDIA_ROOT, "word_docs", str(stripped_file))
        os.makedirs(input_directory, exist_ok=True)
        
        #Reading the excel sheet for creating receipts
        file_path = os.path.join(settings.MEDIA_ROOT,"upload",file)
        values = pd.read_excel(file_path)
        slot_no = values["S No"]
        
        #Setting the receipt details
        doc = DocxTemplate(os.path.join(settings.MEDIA_ROOT,"format","Receipt_Format-4.docx"))
        for i in range(len(slot_no)):
            context = { 'donor_name' : values["Name of the Donor"][i],
                        'donor_address': values["Address"][i],
                        'donor_pan': values["PAN No."][i],
                        'donation_amount': values["Donation Amount	"][i],
                        'date': values["Donation Date"][i],
                        'receipt_no': values["Receipt No."][i]
                        }
            doc.render(context)
            final_path=  os.path.join(settings.MEDIA_ROOT,"word_docs",stripped_file,str(slot_no[i]) + "_receipt.docx")
            doc.save(final_path)

        #Using microsoft word specific docx2pdf lib
        output_dir = os.path.join(settings.MEDIA_ROOT, "pdf", str(stripped_file))
        os.makedirs(output_dir, exist_ok=True)
        #pythoncom to give python access to word
        pythoncom.CoInitialize()
        convert(input_directory,output_dir)

        return JsonResponse({'message':'Receipts generated successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def delete_receipt(request,file):
    try:
        #Checkinf if the receipts exist or not
        stripped_file = os.path.splitext(file)[0]
        pdf_path = os.path.join(settings.MEDIA_ROOT, "pdf", stripped_file)
        word_docs_path = os.path.join(settings.MEDIA_ROOT, "word_docs", stripped_file)

        if not (os.path.exists(pdf_path) or os.path.exists(word_docs_path)):
            raise FileNotFoundError(f"File not found: {file}")
        
        #Recursively deleting them
        shutil.rmtree(pdf_path)
        shutil.rmtree(word_docs_path)
        return JsonResponse({'message': 'Receipts deleted successfully'})

    except FileNotFoundError as e:
        return JsonResponse({'error': 'Receipts have not been generated for this file'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def upload_file(request):
    try:
        myfile = request.FILES['uploaded_file']
        if (os.path.exists(os.path.join(settings.MEDIA_ROOT,"upload",myfile.name))):
            raise FileExistsError
        # Save the file to the media directory
        fs = FileSystemStorage()
        fs.save(myfile.name, myfile)

        # Define the destination directory (/media/upload)
        destination_directory = os.path.join(settings.MEDIA_ROOT, 'upload')
        os.makedirs(destination_directory, exist_ok=True)

        # Moving the path from old location to new one
        uploaded_file_path = os.path.join(settings.MEDIA_ROOT,myfile.name)
        destination_file_path = os.path.join(destination_directory,myfile.name)
        os.rename(uploaded_file_path, destination_file_path)
        return JsonResponse({'message':'File uploaded successfully'})
    except FileExistsError as e:
        return JsonResponse({'error': "File already exists, Upload a differnent one"}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def send_email(request,dir):
    try:
        #Getting values from excel doc
        values = pd.read_excel(os.path.join(settings.MEDIA_ROOT,"upload",dir + ".xlsx"))
        slot_no = values["S No"]
        emails = values["Email Address"]

        #Email details from sqlite
        email_details = Email.objects.all() 
        body = MIMEText(email_details[0].body) # convert the body to a MIME compatible string
        subject = email_details[0].subject
        sender = email_details[0].sender
        password = email_details[0].app_password
        
        for i in range(len(slot_no)):
            # if i == 1:
            #     return JsonResponse({'message':'Email sent successfully'})
            
            #Adding the email details
            msg = MIMEMultipart()
            msg.attach(body)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = emails[i]
            pdf = os.path.join(settings.MEDIA_ROOT,"pdf",dir,str(slot_no[i]) + "_receipt.pdf")
            
            #Adding the file to the email
            with open(pdf, "rb") as pdf_file:
                pdf_attachment = MIMEApplication(pdf_file.read())
                pdf_attachment.add_header('Content-Disposition', 'attachment', filename= str(slot_no[i]) + "_receipt.pdf")
                msg.attach(pdf_attachment)
            
            #Sedning email to gmail smtp server
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, emails[i], msg.as_string())

        return JsonResponse({'message':'Email sent successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    