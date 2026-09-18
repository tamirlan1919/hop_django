from django.contrib import admin
from django.db.models import Avg, Count

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock',
                    'orders_count', 'avg_rating', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    actions = ['activate', 'deactivate']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _orders_count=Count('order_items', distinct=True),
            _avg_rating=Avg('reviews__rating'),
        )

    @admin.display(description='Продано', ordering='-_orders_count')
    def orders_count(self, obj):
        return obj._orders_count

    @admin.display(description='Рейтинг', ordering='-_avg_rating')
    def avg_rating(self, obj):
        return round(obj._avg_rating, 2) if obj._avg_rating else '-'

    @admin.action(description='Активировать выбранные')
    def activate(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активировано: {updated}')

    @admin.action(description='Снять с публикации')
    def deactivate(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Снято: {updated}')
