from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListPost.as_view()),
    path('/detail', views.DetailPost.as_view()),
    path('posts/<int:pk>/increase_count/', views.IncreaseCount.as_view(), name='increase-count'),
    # path('kakao-login/', views.kakao_login, name='kakao-login'),

    path('kakaoLoginLogic/', views.kakaoLoginLogic, name='kakao-login-logic'),
    path('accounts/kakao/login/callback/', views.kakaoLoginLogicRedirect, name='kakao-login-callback'),
    path('kakaoLogout/', views.kakaoLogout, name='kakao-logout'),
]
