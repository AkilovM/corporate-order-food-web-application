from django.contrib import admin
from .models import Person, Food, Order, Food_Order

# Register your models here.
admin.site.register(Person)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(Food_Order)
