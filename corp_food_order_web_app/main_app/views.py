from django.shortcuts import render
from .models import Person, Food, Order, Food_Order
from .forms import Order_Form

# Create your views here.
def index(request):
    create_test_values()
    persons = Person.objects.all()
    menu = Food.objects.all()
    order_form = Order_Form()
    return render(request, 'index.html', {'persons':persons, 'menu':menu, 'order_form':order_form})

def create_order(request):
    if request.method == 'POST':
        order = Order()
        order.date = request.POST.get('date')
        order.person = request.POST.get('person')
        order.save()

        food_list = request.POST.get('food_list')
        for food in food_list:
            food_order = Food_Order()
            food_order.food = food
            food_order.order = order
            food_order.amount = food.amount
            food_order.save()
        # return ...
        
#TODO
#def get_report(request):

def create_test_values():
    if Person.objects.all().count() == 0:
        for name in ['Александр', 'Евгения', 'Юрий', 'Юлия', 'Иван', 'Мария']:
            Person.objects.create(name=name)
    if Food.objects.all().count() == 0:
        Food.objects.create(name='Суп', ingredients='Вода 200мл, Капуста, Морковь, Вода 200мл, Капуста, Морковь, Вода 200мл, Капуста, Морковь.', price=50.99)
        Food.objects.create(name='Салат', ingredients='Огурец, Помидор, Капуста, Лук', price=40.49)
        Food.objects.create(name='Чай', ingredients='Заварка, Сахар.', price=7.50)
    if Order.objects.all().count() == 0:
        person = Person.objects.all()[0]
        Order.objects.create(date='2023-01-01', person=person)
    if Food_Order.objects.all().count() == 0:
        menu = Food.objects.all()
        order = Order.objects.all()[0]
        food_order = Food_Order.objects.create(food=menu[0], order=order, amount=1)
        food_order = Food_Order.objects.create(food=menu[1], order=order, amount=2)
        food_order = Food_Order.objects.create(food=menu[2], order=order, amount=3)
