from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('overview/', views.overview),
    path('overview/platform_info/', views.overview_platform),
    path('overview/eda/', views.overview_eda),
    path('login/', views.login),
    path('search/category/', views.search_category),
    path('search/detail/', views.search_detail),
    path('profile/', views.profile),
    path('community/', views.community),
    path('community/create', views.community_create),
    path('support/', views.support),
    path('signup/', views.signup)
]