from django.contrib import admin

from notmeat_app.models import (
    Dish,
    DishCategory,
    Order,
    Payment,
)

# Register your models here.
#
admin.site.register(DishCategory)
admin.site.register(Dish)
admin.site.register(Order)
admin.site.register(Payment)
