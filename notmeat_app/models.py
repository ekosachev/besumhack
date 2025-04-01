from django.db import models
from random import choice

from .cursed_payment_reasons import CURSED_PAYMENT_REASONS, DEFAULT_PAYMENTS
from django.contrib.auth.models import User

# Create your models here.


class DishCategory(models.Model):
    name = models.CharField(blank=False, max_length=256)


class Dish(models.Model):
    category = models.ForeignKey(
        DishCategory, on_delete=models.CASCADE, related_name="dishes"
    )
    name = models.CharField(max_length=256)
    contents = models.CharField(max_length=1024)

    image = models.ImageField(upload_to="./dish_images")


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(blank=True)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="orders")


class Payment(models.Model):
    is_optional = models.BooleanField()
    amount = models.FloatField()
    reason = models.CharField(max_length=256)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")

    @classmethod
    def generate_cursed_payment(cls, order: Order) -> "Payment":
        reason, amount = choice(CURSED_PAYMENT_REASONS)
        return Payment(
            is_optional=True,
            amount=amount,
            reason=reason,
            order=order,
        )

    @classmethod
    def generate_default_payments(cls, order: Order) -> list["Payment"]:
        return [
            Payment(
                is_optional=True,
                amount=amount,
                reason=reason,
                order=order,
            )
            for reason, amount in DEFAULT_PAYMENTS
        ]
