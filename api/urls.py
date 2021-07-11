from django.urls import path
from . import views


urlpatterns = [
    path('company-login/', views.CompanyLogin.as_view(), name='login'),
    path('company-create/', views.CompanyCreate.as_view(), name='register'),
    path('company/', views.CompanyGPDP.as_view(), name='create-cgud'),
    path('all-companies/', views.CompanyGP.as_view(), name='company-gp'),
    path('service-area/', views.ServiceAreaPG.as_view(), name='service-pg'),
    path('my-service-area/<uuid:service_area_id>/',
         views.ServiceAreaGPD.as_view(), name='service-gpd'),
    # path('search/', SearchServiceArea.as_view(), name='search-service-area')
]
