from django.db import models
from random import choice

from .cursed_payment_reasons import CURSED_PAYMENT_REASONS, DEFAULT_PAYMENTS
from django.contrib.auth.models import User

# Create your models here.


class DishCategory(models.Model):
    name = models.CharField(blank=False, max_length=256)


class Dish(models.Model):
    contents = models.CharField(max_length=1024)
    mass = models.FloatField()


class DishInSet(models.Model):
    amount = models.IntegerField()
    dish = models.ForeignKey(
        Dish, on_delete=models.CASCADE, related_name="dish_in_sets"
    )
    dish_set = models.ForeignKey(
        "DishSet", on_delete=models.CASCADE, related_name="dishes_in_set"
    )


class DishSet(models.Model):
    name = models.CharField(max_length=256)
    dishes = models.ManyToManyField(
        to=Dish, through=DishInSet, related_name="dish_sets"
    )
    price = models.FloatField()
    picture = models.ImageField(upload_to="dish_images/")
    category = models.ForeignKey(
        DishCategory, on_delete=models.CASCADE, related_name="dish_sets"
    )


class DishSetInOrder(models.Model):
    amount = models.IntegerField()
    dish_set = models.ForeignKey(
        DishSet, on_delete=models.CASCADE, related_name="dish_set_in_orders"
    )

    order = models.ForeignKey(
        "Order",
        on_delete=models.CASCADE,
        related_name="dish_sets_in_order",
    )


class DeliveryAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    latitude = models.FloatField()
    longitute = models.FloatField()


ORDER_STATUS_CHOICES = {
    "CR": "Created",
    "PR": "Payment received",
    "CK": "Cooking",
    "DL": "Delivering",
    "FN": "Finished",
}


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(blank=True)
    dish_sets = models.ManyToManyField(
        DishSet, through=DishSetInOrder, related_name="orders"
    )
    status = models.CharField(choices=ORDER_STATUS_CHOICES, max_length=2)
    delivery_address = models.ForeignKey(
        DeliveryAddress, on_delete=models.CASCADE, related_name="orders"
    )

    def generate_dish_payments(self) -> list["Payment"]:
        result = []
        for dish_set_in_order in self.dish_sets.all():
            result.append(
                Payment(
                    is_optional=False,
                    amount=dish_set_in_order.dish_set.price,
                    reason=dish_set_in_order.dish_set.name,
                    dish_set=dish_set_in_order.dish_set,
                    order=self,
                )
            )

        return result


class Payment(models.Model):
    is_optional = models.BooleanField()
    amount = models.FloatField()
    reason = models.CharField(max_length=256)
    dish_set = models.ForeignKey(
        DishSet, on_delete=models.SET_NULL, related_name="payments", null=True
    )

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
