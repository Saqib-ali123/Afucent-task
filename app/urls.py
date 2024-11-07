from django.contrib import admin
from django.urls import path,include
from app.views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_get'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/',user),
    path('login/',LoginView.as_view()),
    path('logout/',logoutView.as_view()),
    path('task/<int:id>/',taskview.as_view()),
    path('task/',taskview.as_view()),

]