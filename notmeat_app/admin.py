from django.contrib import admin

from notmeat_app.models import (
    DeliveryAddress,
    Dish,
    DishCategory,
    DishSet,
    Order,
    Payment,
)

# Register your models here.
#
admin.site.register(DishCategory)
admin.site.register(Dish)
admin.site.register(DishSet)
admin.site.register(DeliveryAddress)
admin.site.register(Order)
admin.site.register(Payment)
