from django.urls import path
from .views import FarmersManagementDetailView, FarmersManagementListView, MilkRecordsDetailView, MilkRecordsListView, CooperativeList, SaccoList, SaccoDetail , ScoreDetailView, ScoreListView
from .views import SignupView, LoginView, LogoutView, AdminOnlyView, SaccoOnlyView, CooperativeOnlyView
from . import views


urlpatterns = [
    path("farmers/", FarmersManagementListView.as_view(), name="farmersmanagement_list_view"),
    path("milk-records/" ,MilkRecordsListView.as_view(),name="milk_records_list_view"),
    path("milk-records/<int:farmers_id>/" ,MilkRecordsDetailView.as_view(),name="milk_records_detail_view"),
    path('farmers/<int:farmers_id>/', FarmersManagementDetailView.as_view(), name='farmers_detail_view') ,
    path('sacco/', SaccoList.as_view(), name='sacco-list'),
    path('sacco/<int:sacco_id>/', SaccoDetail.as_view(), name='sacco-detail'),
    path('cooperative/', CooperativeList.as_view(), name='cooperative-list'),
    path("credit-scores/", ScoreListView.as_view(), name="credit_score_list"),
    path("credit-scores/<int:farmer_id>/", ScoreDetailView.as_view(), name="score_detail"),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),
    path('sacco-only/', SaccoOnlyView.as_view(), name='sacco_only'),
    path('cooperative-only/', CooperativeOnlyView.as_view(), name='cooperative_only'),
    path('generate_token/', views.generate_token, name='generate_token'),
]