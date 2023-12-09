from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView

from .views import post_views, login_views, views

urlpatterns = [
    path('', post_views.ListPost.as_view()),
    path('<int:pk>', post_views.DetailPost.as_view()),
    path('posts/<int:pk>/increase_count/', post_views.IncreaseCount.as_view(), name='increase-count'),
    # path('kakao-login/', views.kakao_login, name='kakao-login'),

    # path('kakaoLoginLogic/', views.kakaoLoginLogic, name='kakao-login-logic'),
    # path('accounts/kakao/login/callback/', views.kakaoLoginLogicRedirect, name='kakao-login-callback'),
    # path('kakaoLogout/', views.kakaoLogout, name='kakao-logout'),

    path("login", login_views.try_login, name = 'try_login'),
    # path("verifyuser", login_views.verify_user, name = 'code'),
    # path("logout", login_views.logout, name = 'logout'),
    path("nickname", login_views.set_nickname, name ="set_nickname"),
    path('api/token', login_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
