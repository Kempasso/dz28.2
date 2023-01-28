from django.contrib import admin
from django.urls import path
from ads import views
from ads.views import AdsDetailView, CategoryDetailView, CatListView

urlpatterns = [
    path('', CatListView.as_view()),
    path('<int:pk>', CategoryDetailView.as_view()),
    ]