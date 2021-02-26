from django.urls import path
from . import views

app_name = 'recommend'

urlpatterns = [
    path('worldcup/', views.worldcup, name='worldcup'),
    path('ratings/',views.rating,name='ratings'),
]
