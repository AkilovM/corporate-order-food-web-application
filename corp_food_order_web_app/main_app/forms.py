from django import forms
from .models import Person, Food, Order, Food_Order

# Represent person as person.name
class Person_ModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class Order_Form(forms.Form):
    #person = forms.ModelChoiceField(queryset=Person.objects.all())
    person = Person_ModelChoiceField(queryset=Person.objects.all(), label='Кто вы?')
    date = forms.DateField(widget=forms.SelectDateWidget(), label='Дата заказа:')
    food_list = forms.ModelMultipleChoiceField(queryset=Food.objects.all(), label='Меню')
