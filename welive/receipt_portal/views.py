from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import glob


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
        
        #Displaying the uploaded files
        directory = settings.MEDIA_ROOT + "/"
        files = glob.glob(settings.MEDIA_ROOT+"/*")
        options = [file.replace(directory, '') for file in files]
        return render(request,'main/home.html', {
                'test': options
            })