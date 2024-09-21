from django.urls import path

from views import CertificatesListCreateView, CertificatView

app_name = 'users'

urlpatterns = [
    path('', CertificatesListCreateView, name='certificates_list'),
    path('<id: int>/', CertificatView, name='certificate'),
    
]