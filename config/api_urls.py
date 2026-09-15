from rest_framework.routers import DefaultRouter

import orders
from orders.api_views import OrderViewSet
from products.api_views import ProductViewSet, CategoryViewSet

router = DefaultRouter()

router.register('orders', OrderViewSet, basename='order')
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet, basename='category')


