from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('marketplace/', views.marketplace, name="marketplace"),
    path('sell/', views.sell, name="sell"),
    path('dataset/<int:id>/', views.detail_dataset, name='detail-dataset'),
    path('detail-submit/<int:pk>/', views.detail_submit, name='detail-submit'),
    path('contact/', views.contact, name='contact'),
]