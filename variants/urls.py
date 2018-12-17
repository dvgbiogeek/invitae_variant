from django.urls import path

from variants import views

app_name = 'variants'
urlpatterns = [
    path('', views.index, name='index'),
]
