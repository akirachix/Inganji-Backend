from django.urls import path,re_path
from .views import FarmersManagementDetailView, FarmersManagementListView, MilkRecordsDetailView, MilkRecordsListView, CooperativeList, SaccoList, SaccoDetail , ScoreDetailView, ScoreListView
from .views import SignupView, LoginView, LogoutView, AdminOnlyView, SaccoOnlyView, CooperativeOnlyView
from . import views
from .views import ScoreCreateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import PredictView
import predictive_model.views as views

schema_view =get_schema_view (
    openapi.Info (
        title= "InganjiFanikisha API",
        default_version='v1',
        description="Api documentation  for Fanikisha project",
        terms_pf_service="https://fanikisha-3beb7fcefffe.herokuapp.com/auth/",
        contact=openapi.Contact(email="wanjiruwanjikuivy@gmail.com"),
        license=openapi.License(name="BSD License"),

    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("farmers/", FarmersManagementListView.as_view(), name="farmersmanagement_list_view"),
    path("milk-records/" ,MilkRecordsListView.as_view(),name="milk_records_list_view"),
    path("milk-records/<int:farmer_id>/" ,MilkRecordsDetailView.as_view(),name="milk_records_detail_view"),
    path('farmers/<int:farmer_id>/', FarmersManagementDetailView.as_view(), name='farmers_detail_view') ,
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
    path('scores/', ScoreCreateView.as_view(), name='create_score'),
    path('predict/', PredictView.as_view(), name='predict'),


]


