from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.handleSignUp, name='handleSignUp'),
    path('login/', views.handeLogin, name="handleLogin"),
    path('logout/', views.handleLogout, name="handleLogout"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('search/', views.search, name="Search"),
    path('checkout/', views.checkout, name="Checkout"),
    path('productView/<int:myid>', views.productView, name="productView"),
    path('orderView/', views.orderView, name="orderView"),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),

]