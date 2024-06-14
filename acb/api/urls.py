from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


app_name = 'acb-api'

router = routers.DefaultRouter()
# router.register(r'pbp-lean', views.PbpLeanView, basename='pbp-lean')

urlpatterns = [
    path('', include(router.urls)),
    path('pbp-lean/<int:game_id>/', views.PbpLeanView.as_view(), name='pbp-lean'),
    path('game-leaders/<int:game_id>/', views.GameLeadersView.as_view(), name='game-leaders'),
    path('game-biggest-lead/<int:game_id>/', views.GameBiggestLeadView.as_view(), name='game-biggest-lead'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
