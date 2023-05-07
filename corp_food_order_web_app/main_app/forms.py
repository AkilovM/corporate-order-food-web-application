from django import forms
from .models import Person, Food, Order, Food_Order

# Represent person as person.name
class Person_ModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class Food_Amount():
    def __init__(self, food, amount):
        self.food = food
        self.amount = amount

class Food_Count_Fields(forms.MultiValueField):
    def __init__(self, **kwargs):
        fields = []
        for i in Food.objects.all():
            fields.append(forms.IntegerField(min_value=0, max_value=99))
        fields = tuple(fields)

class Order_Form(forms.Form):
    person = Person_ModelChoiceField(queryset=Person.objects.all(), label='Ваше имя:')
    date = forms.DateField(widget=forms.SelectDateWidget(), label='Дата заказа:')

    fields = []

    food_list = []
    menu = Food.objects.all()
    for food in menu:
        food_amount_dict = dict()
        food_amount_dict['food'] = food
        food_amount_dict['amount'] = forms.IntegerField(min_value=0, max_value=99)
        #food_list.append(Food_Amount(food, forms.IntegerField(min_value=0, max_value=99)))
        food_list.append(food_amount_dict)
        fields.append(forms.IntegerField(min_value=0, max_value=99))


    amount_fields = forms.MultiValueField(fields=fields)



            
