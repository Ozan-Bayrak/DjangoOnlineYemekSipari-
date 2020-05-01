from django.urls import path

from . import views

urlpatterns = [
    # ex: /restaurant/
    path('', views.index, name='index'),
    path('addtocart/<int:id>',views.addtocart, name='addtocart'),
    path('deletefromcart/<int:id>',views.deletefromcart, name='deletefromcart'),

    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
]