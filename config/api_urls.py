from rest_framework.routers import DefaultRouter

from orders.api_views import OrderViewSet
from products.api_views import CategoryViewSet, ProductViewSet

router = DefaultRouter()

router.register('orders', OrderViewSet, basename='order')
router.register('products', ProductViewSet, basename='product')
router.register('categories', CategoryViewSet, basename='category')


