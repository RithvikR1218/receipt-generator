from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.

def say_hello(request):
    
    return render(request,'hello.html',{'Name':'Rithvik'})

def home(request):
    if not request.user.is_authenticated: #if the user is not authenticated
        return HttpResponseRedirect(reverse("login")) #redirect to login page
    else:
        #Logic for uploading files
        if request.method == 'POST' and request.FILES['myfile']:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            return render(request, 'main/home.html', {
                'uploaded_file_url': uploaded_file_url
            })
        return render(request,'main/home.html')