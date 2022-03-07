from django.urls import path
from .views import SendPinView

urlpatterns = [
    path('/pins', SendPinView.as_view()),
]
