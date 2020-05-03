from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from home.models import UserProfile
from order.models import ShopCartForm, ShopCart, OrderForm, Order, OrderProduct
from restaurant.models import Category, Foods


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
            request.session['cart_items']=ShopCart.objects.filter(user_id=current_user.id).count() #count item in shopcart

            return HttpResponseRedirect(url)

    messages.warning(request,"Ürün eklemede hata oluştu!!.Lütfen Kontrol ediniz.")
    return HttpResponseRedirect(url)

@login_required(login_url='/login')
def shopcart(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    category = Category.objects.all()
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # count item in shopcart
    total = 0
    for rs in shopcart:
        total += rs.food.price * rs.quantity

    context = {'shopcart': shopcart,
               'total':total,'category':category}

    return render(request,'Shopcart_food.html',context)

@login_required(login_url='/login') #check login
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()  # count item in shopcart
    messages.success(request,"Ürün Sepetten Silinmiştir.")
    return HttpResponseRedirect("/shopcart")


@login_required(login_url='/login') #check login
def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    scart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in scart:
        total += rs.food.price * rs.quantity

    if request.method == 'POST': #if there is a post
        form = OrderForm(request.POST)

        if form.is_valid():
            data =Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            #Move shopcart items to order products items
            scart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in scart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.restaurant_id = rs.food.restaurant_id
                detail.foods_id = rs.food_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price  = rs.food.price
                detail.amount = rs.amount
                detail.save()

            ShopCart.objects.filter(user_id=current_user.id).delete() #clear shopcart
            request.session['cart_items']=0
            return render(request,'Order_Completed.html',{'ordercode':ordercode,'category':category})

        else:
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'scart':scart,
        'category':category,
        'total':total,
        'form':form,
        'profile':profile
    }
    return render(request,'Order_Form.html',context)







