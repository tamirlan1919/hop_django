from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from django.db import transaction


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_price', 'shipping_address', 'created_at', 'items']


class OrderItemWriteSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()
    items = OrderItemWriteSerializer(many=True)

    def validate_items(self, data):
        if not data:
            raise serializers.ValidationError('Заказ должен содержать хотя бы один элемент')
        return data

    def create(self, validated_data):
        user = self.context['request'].user

        with transaction.atomic():
            order = Order.objects.create(
                user=user,
                status = Order.Status.PAID,
                shipping_address = validated_data['shipping_address'],
                total_price=0
            )
            total = 0
            for item in validated_data['items']:
                product = (
                    Product.objects.get(id=item['product_id'])
                )
                if product.stock < item['quantity']:
                    raise serializers.ValidationError(f'Не хватает кол-во {product.name} на складе')

                product.stock -= item['quantity']
                product.save(update_fields=['stock'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price,
                )
                total += product.price * item['quantity']
            order.total_price = total
            order.save(update_fields=['total_price'])
            return order

