from django.urls import path

from .views import Home, StaffDashboard, ProductDetails, CategorytDetails, ProudctList, SearchProducts

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('staff/', StaffDashboard.as_view(), name='staff_dashboard'),  # New URL for staff dashboard
    path('product-details/<str:slug>/', ProductDetails.as_view(), name='product-details'),
    path('category-details/<str:slug>/', CategorytDetails.as_view(), name='category-details'),
    path('product-list/', ProudctList.as_view(), name='product-list'),
    path('search-products/', SearchProducts.as_view(), name='search-products'),
]