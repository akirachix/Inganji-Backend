from django.urls import path
from .views import FarmersManagementDetailView, FarmersManagementListView, MilkRecordsDetailView, MilkRecordsListView, CooperativeList, SaccoList, SaccoDetail  ScoreDetailView,ScoreListView

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




]