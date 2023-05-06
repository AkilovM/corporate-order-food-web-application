from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=30)

class Food(models.Model):
    name = models.CharField(max_length=30)
    ingredients = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    

class Order(models.Model):
    date = models.DateField()
    person = models.ForeignKey(Person, on_delete = models.CASCADE)

class Food_Order(models.Model):
    food = models.ForeignKey(Food, on_delete = models.CASCADE)
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    amount = models.PositiveSmallIntegerField()
