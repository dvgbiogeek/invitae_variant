from django.urls import path, include

from rest_framework import routers

from variants import views


# router = routers.DefaultRouter()
# router.register('gene', views.GeneViewSet)


app_name = 'variants'
urlpatterns = [
    path('', views.index, name='index'),
    # path('gene', views.GeneViewSet)
]
