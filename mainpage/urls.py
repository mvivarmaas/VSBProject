from django.urls import path

from . import views

urlpatterns = [
    path('blue', views.blue, name='blue'),
    path('class/<int:term>/<slug:class_name>', views.classfinder, name="classfinder"),
    path('', views.index, name='index'),
    path('account', views.account, name="account"),
    path('API', views.API, name="API"),
    path('contact', views.contact, name="contact"),
    path('API/<int:term>/<slug:slug>', views.API_GET, name="API_GET")

]
