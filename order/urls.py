from django.urls import path

from .views import(
    Checkout,
    SaveOrder,
    Orders
)

urlpatterns = [
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('save-order/', SaveOrder.as_view(), name='save-order'),
    path('orders/', Orders.as_view(), name='orders'),
]