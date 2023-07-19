from django.urls import path
from certificates.views import generate_certificate, verify_certificate, download_certificate

urlpatterns = [
    path('generate/', generate_certificate, name='generate_certificate'),
    path('verify/<str:token>/', verify_certificate, name='verify_certificate'),
    path('download/<int:certificate_id>/', download_certificate, name='download_certificate'),
]
