from django.urls import path
from .views import (
    RegisterPenjualView,
    RegisterPembeliView,
    LoginPembeliView,
    LoginPenjualView
)

urlpatterns = [
    path('register/penjual/', RegisterPenjualView.as_view()),
    path('register/pembeli/', RegisterPembeliView.as_view()),
    path('login/penjual/', LoginPenjualView.as_view()),
    path('login/pembeli/', LoginPembeliView.as_view()),
]
