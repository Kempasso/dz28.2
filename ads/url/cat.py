from django.contrib import admin
from django.urls import path
from ads import views
from ads.views import AdDetailView, CategoryDetailView, CatListView, CatCreateView, CatUpdateView, CatDeleteView

urlpatterns = [
    path('', CatListView.as_view()),
    path('<int:pk>', CategoryDetailView.as_view()),
    path('create/', CatCreateView.as_view()),
    path('update/<int:pk>/', CatUpdateView.as_view()),
    path('delete/<int:pk>/', CatDeleteView.as_view()),
    ]