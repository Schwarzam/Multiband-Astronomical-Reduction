from django.urls import path, include
from .views import RegisterAPI, LoginAPI, UserAPI
from knox import views as knox_views


urlpatterns = [
    path('reduction/auth', include('knox.urls')),
    path('reduction/auth/register', RegisterAPI.as_view()),
    path('reduction/auth/login', LoginAPI.as_view()),

    path('reduction/auth/user', UserAPI.as_view()),

    path('reduction/auth/logout', knox_views.LogoutView.as_view(), name="knox_logout"),
]