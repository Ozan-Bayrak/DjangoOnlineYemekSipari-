from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from restaurant.models import CommentForm, Comment


def index(request):
    return HttpResponse("Restaurant Page")

@login_required(login_url='login') #login check
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    if request.method == 'POST': #form post edildiyse
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user=request.user #Acces User Session information
            data=Comment() #model ile bağlantı kur
            data.user_id = current_user.id
            data.restaurant_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save() # kaydet
            messages.success(request,"Yorumunuz başarı ile gönderilmiştir.Teşekkür ederiz")
            return HttpResponseRedirect(url) #kaydedildi
    messages.error(request, "Yorumunuz Kaydedilemedi! Lütfen kontrol ediniz.")
    return HttpResponseRedirect(url) #kaydedildi