from django.urls import path
from . import views
from progressiveApp.views import home


urlpatterns = [
    path('', home, name='home'),
    path('home/', views.homepage, name='homepage'),

    path('about/',  views.about, name='homepage/about'),
    path('contact/', views.contact, name='homepage/contact'),
    path('services/', views.services, name='homepage/services'),
    path('pricing/', views.price, name='homepage/pricing'),
    path('price/', views.price, name='homepage/price'),
    path('error/', views.error, name='homepage/error'),
    path('team/', views.team, name='homepage/team'),
    path('signin/', views.signin, name='homepage/signin'),
    path('signup/', views.signup, name='homepage/signup'),
    path('subscibe/', views.is_subscribed, name='homepage/subscibe'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('getcode/', views.request_verification, name='getcode',)
]