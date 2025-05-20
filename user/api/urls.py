from django.urls import path
from user.api.views import RegisterView, VerifyEmailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
]