from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from order.models import ShopCartForm, ShopCart
from restaurant.models import Category


def index(request):
    return HttpResponse("Order App")

@login_required(login_url='/login') #check login
def addtocart(request,id):
    url = request.META.get('HTTP_REFERER') #get last url
    current_user = request.user  # accsess user session info

    check = ShopCart.objects.filter(food_id=id) #ürün sepette varmı
    if check:
        control = 1 #ürün sepette var
    else:
        control = 0 #ürün sepette yok
    if request.method == 'POST': #method post edildiyse
        form = ShopCartForm(request.POST)
        if form.is_valid():

            if control == 1: #ürün varsa güncelle
                data = ShopCart.objects.get(food_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save() #DB kaydet
            else :
                data = ShopCart() #model ile bağlantı kur
                data.user_id = current_user.id
                data.food_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save() # DB kaydet

            messages.success(request,'Ürün Sepete Eklendi.')

            return HttpResponseRedirect(url)

    messages.warning(request,"Ürün eklemede hata oluştu!!.Lütfen Kontrol ediniz.")
    return HttpResponseRedirect(url)

@login_required(login_url='/login')
def shopcart(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    category = Category.objects.all()
    total = 0
    for rs in shopcart:
        total += rs.food.price * rs.quantity

    context = {'shopcart': shopcart,
               'total':total,'category':category}

    return render(request,'Shopcart_food.html',context)

@login_required(login_url='/login') #check login
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request,"Ürün Sepetten Silinmiştir.")
    return HttpResponseRedirect("/shopcart")
