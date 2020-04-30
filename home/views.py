import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, JoinForm
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

def restaurants_detail(request, id):
    restaurant = Restaurant.objects.get(pk=id)
    images = Images.objects.filter(restaurant_id=id)
    foods = Foods.objects.filter(restaurant_id=id)
    comments = Comment.objects.filter(restaurant_id=id,status='True')
    context = {'restaurant': restaurant, 'images': images, 'foods': foods,'comments':comments }
    return render(request, 'restaurants_detail.html', context)

def food_search(request):
    if request.method == 'POST': #form post edildiyse
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query'] #formdan bilgiyi al
            foods = Foods.objects.filter(title__icontains=query) #Select * from food where title like %query%
            restaurant = Restaurant.objects.all()[:1]
            #return HtttpResponse(foods)
            context = {'foods':foods,
                       'category':category,
                       'restaurant':restaurant}
            return render(request,'foods_search.html',context)
    return HttpResponseRedirect('/')

def food_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        food = Foods.objects.filter(city__icontains=q)
        results = []
        for rs in food:
            food_json = {}
            food_json = rs.title
            results.append(food_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Login Hatası ! Kullanıcı adı yada şifre hatalı.")
            return HttpResponseRedirect('/login')
    return render(request,'login.html')

def join_view(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username,password=password)
        login(request,user)
        return HttpResponseRedirect('/')
    form = JoinForm()
    context = {'form':form,}
    return render(request, 'join.html',context)