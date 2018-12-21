from django.urls import path

from variants import views


app_name = 'variants'
urlpatterns = [
    path('api/', views.GeneVariantInfoAllList.as_view()),
    path('api/<str:gene>', views.GeneList.as_view()),
    path('api/variants/<str:gene>', views.GeneVariantInfoList.as_view()),
]
