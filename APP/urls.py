from . import views
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login),
    path('register', views.register),
    path('member', views.member),
    path('district_administrator', views.district_administrator),
    path('funding_administrator', views.funding_administrator),
    path('register_FA', views.register_FA),
    path('register_DA', views.register_DA),
    path('logout', views.logout),
    path('success', views.success),
    path('application', views.application),
    path('da_actions', views.da_actions),
    path('fa_actions', views.fa_actions),
    path('user_profile_fa/<int:id>/', views.user_profile_fa),
    path('user_profile_da/<int:id>/', views.user_profile_da),
]

