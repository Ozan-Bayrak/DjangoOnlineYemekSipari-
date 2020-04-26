from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactForm, ContactFormMessage
from restaurant.models import Foods, Category, Restaurant, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Foods.objects.all()[:5]
    category = Category.objects.all()
    lastrestaurants = Restaurant.objects.all().order_by('-id')[:6]

    context = {'setting': setting,
               'category': category,
               'page': 'home',
               'sliderdata': sliderdata,
               'lastrestaurants': lastrestaurants}
    return render(request, 'index.html', context)


def restaurants(request):
    restaurant = Restaurant.objects.all()
    context = {'restaurant': restaurant}
    return render(request, 'restaurants.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'aboutus'}
    return render(request, 'aboutus.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']  # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veri tabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmiştir.Teşekkür ederiz.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    form = ContactForm()
    context = {'setting': setting, 'form': form}
    return render(request, 'contact.html', context)


def restaurants_detail(request, id, title):
    restaurant = Restaurant.objects.get(pk=id)
    images = Images.objects.filter(restaurant_id=id)
    foods = Foods.objects.filter(restaurant_id=id)
    comments = Comment.objects.filter(restaurant_id=id,status='True')
    context = {'restaurant': restaurant, 'images': images, 'foods': foods,'comments':comments }
    return render(request, 'restaurants_detail.html', context)
