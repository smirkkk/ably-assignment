from django.urls import path
from .views import SignupView, SendPinView, CertifyPhoneView, LoginView

urlpatterns = [
    path('', SignupView.as_view()),
    path('/pins', SendPinView.as_view()),
    path('/phones', CertifyPhoneView.as_view()),
    path('/login', LoginView.as_view())
]
