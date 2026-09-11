from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction

from products.models import Product
from .cart import Cart
from .models import OrderItem, Order


class OutOfStock(Exception):
    pass


@transaction.atomic
def create_order(user, cart, data) -> Order:
    order = Order.objects.create(
        user=user,
        status=Order.STATUS_PAID,
        shipping_address=(
            f'{data["full_name"]}, {data["phone_number"]}\n'
            f'{data["city"]}, {data["address"]}\n'
        )
    )
    total = 0
    for item in cart:
        product = Product.objects.get(id=item["product_id"])
        if product.stock < item["quantity"]:
            raise OutOfStock(f'Не хватает {product.name} на складе')
        product.stock -= item["quantity"]
        product.save(update_fields=['stock'])

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item["quantity"],
            price=item["price"],

        )
        total += item["price"]
    order.total = total
    order.save(update_fields=['total_price'])
    return order


def send_order_email(order: Order) -> None:
    send_mail(
        subject=f'Hop & Barley - заказ {order.id}',
        message='....',
        from_email=settings.DEFAULT_FROM_EMAIL,

    )

