from django.urls import path
from .views import SignupView, LoginView, LogoutView, AdminOnlyView, SaccoOnlyView, CooperativeOnlyView
from . import views

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),
    path('sacco-only/', SaccoOnlyView.as_view(), name='sacco_only'),
    path('cooperative-only/', CooperativeOnlyView.as_view(), name='cooperative_only'),
    path('generate_token/', views.generate_token, name='generate_token'),
]