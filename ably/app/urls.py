from django.urls import path
from .views import UserView, SendPinView, CertifyPhoneView, LoginView, ResetPasswordView

urlpatterns = [
    path('', UserView.as_view()),
    path('/login', LoginView.as_view()),
    path('/passwords', ResetPasswordView.as_view()),
    path('/phones', CertifyPhoneView.as_view()),
    path('/pins', SendPinView.as_view())
]
