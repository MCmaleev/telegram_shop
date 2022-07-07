from django.template.defaulttags import url
from django.urls import path

from main import views

urlpatterns = [
    path('', views.products_list, name='products_list'),

    path('api/makeOrder', views.make_order, name='makeOrder')
]
