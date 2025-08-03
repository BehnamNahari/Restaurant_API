from django.urls import path

from .models import MenuItem
from .views import OrderListCreateView, OrderDetailView, ReservationListCreateView, ReservationDetailView, \
    RatingListCreateView, RatingDetailView, MenuItemListView, MenuItemDetailView

urlpatterns = [
    path('orders/',OrderListCreateView.as_view()),
    path('orders/<int:pk>',OrderDetailView.as_view()),
    path('reservations/',ReservationListCreateView.as_view()),
    path('reservations/<int:pk>',ReservationDetailView.as_view()),
    path('Ratings/',RatingListCreateView.as_view()),
    path('ratings/<int:pk>',RatingDetailView.as_view()),
    path("menu-items/",MenuItemListView.as_view()),
    path("menu-items/<int:pk>",MenuItemDetailView.as_view()),
]
