from typing import Any
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.core.paginator import(
    PageNotAnInteger,
    EmptyPage,
    InvalidPage,
    Paginator
)

from cart.carts import Cart
from .models import (
    Category,
    Product,
    Slider
)
from order.models import *
from django.shortcuts import redirect
from django.views import generic
from datetime import date



class Home(generic.TemplateView):
    template_name = 'home.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('staff_dashboard')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'featured_categories': Category.objects.filter(featured=True),
                'featured_products': Product.objects.filter(featured=True),
                'sliders': Slider.objects.filter(show=True)
            }
        )
        return context

class StaffDashboard(generic.TemplateView):
    template_name = 'staff_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        today_orders_count = Order.objects.filter(created_date__date=today).count()
        context['today_orders_count'] = today_orders_count
        return context


class ProductDetails(generic.DetailView):
    model = Product
    template_name = 'product/product-details.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['related_products'] = product.related
        return context
    
class CategorytDetails(generic.DetailView):
    model = Category
    template_name = 'product/category-details.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['products'] = self.get_object().products.all()
        return context
    
class CustomPaginator:
    def __init__(self, request, queryset, paginated_by) -> None:
        self.paginator = Paginator(queryset, paginated_by)
        self.paginated_by = paginated_by
        self.queryset = queryset
        self.page = request.GET.get('page', 1)

    def get_queryset(self):
        try:
            queryset = self.paginator.page(self.page)
        except PageNotAnInteger:
            queryset = self.paginator.page(1)
        except EmptyPage:
            queryset = self.paginator.page(1)
        except InvalidPage:
            queryset = self.paginator.page(1)

        return queryset
    
class ProudctList(generic.ListView):
    model = Product
    template_name = 'product/product-list.html'
    context_object_name = 'object_list'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = CustomPaginator(self.request, self.get_queryset(), self.paginate_by)
        quryset = page_obj.get_queryset()
        paginator = page_obj.paginator
        context['object_list'] = quryset
        context['paginator'] = paginator
        return context

class SearchProducts(generic.View):
    def get(self, *args, **kwargs):
        key = self.request.GET.get('key', '')
        products = Product.objects.filter(
            Q(title__contains=key) |
            Q(category__title__contains=key)
        )
        context = {
            'products': products,
            "key": key
        }
        return render(self.request, 'product/search-products.html', context)