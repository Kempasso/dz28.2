
from django.urls import path
from ads.views import AdsDetailView, AdsListView

urlpatterns = [
    path('', AdsListView.as_view()),
    path('<int:pk>',  AdsDetailView.as_view()),
    ]