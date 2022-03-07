from django.urls import path
from .views import SendPinView, CertifyPhoneView

urlpatterns = [
    path('/pins', SendPinView.as_view()),
    path('/phones', CertifyPhoneView.as_view())
]
