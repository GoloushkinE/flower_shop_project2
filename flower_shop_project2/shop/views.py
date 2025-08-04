from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from .models import Category, Product
from cart.forms import CartAddProductForm

# Optimized: Cache product list for 5 minutes, vary by language
@cache_page(60 * 5)  # Cache for 5 minutes
@vary_on_headers('Accept-Language')
def product_list(request, category_slug=None):
    category = None
    # Optimize: Use select_related to avoid N+1 queries for translations
    categories = Category.objects.select_related().prefetch_related('translations')
    products = Product.objects.filter(available=True).select_related('category').prefetch_related('translations', 'category__translations')

    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category.objects.prefetch_related('translations'),
                                     translations__language_code=language,
                                     translations__slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


# Optimized: Cache product detail for 10 minutes, vary by language
@cache_page(60 * 10)  # Cache for 10 minutes
@vary_on_headers('Accept-Language')
def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    # Optimize: Use select_related and prefetch_related for better performance
    product = get_object_or_404(Product.objects.select_related('category').prefetch_related('translations', 'category__translations'),
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})