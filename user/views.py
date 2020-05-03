from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import UserProfile
from restaurant.models import Category


def index(request):
    category = Category.objects.all()
    current_user = request.user #access user info
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'profile':profile,'category':category}
    return render(request, 'user_profile.html',context)