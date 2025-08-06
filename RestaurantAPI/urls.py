from django.urls import path

from .models import MenuItem
from .views import OrderListCreateView, OrderDetailView, ReservationListCreateView, ReservationDetailView, \
    RatingListCreateView, RatingDetailView, MenuItemListView, MenuItemDetailView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('reservations/', ReservationListCreateView.as_view(), name='reservation-list'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),

    path('ratings/', RatingListCreateView.as_view(), name='rating-list'),
    path('ratings/<int:pk>/', RatingDetailView.as_view(), name='rating-detail'),

    path('menu-items/', MenuItemListView.as_view(), name='menuitem-list'),
    path('menu-items/<int:pk>/', MenuItemDetailView.as_view(), name='menuitem-detail'),
]
