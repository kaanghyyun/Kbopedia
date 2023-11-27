from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListPost.as_view()),
    path('<int:pk>/', views.DetailPost.as_view()),
    path('posts/<int:pk>/increase_count/', views.IncreaseCount.as_view(), name='increase-count'),
]