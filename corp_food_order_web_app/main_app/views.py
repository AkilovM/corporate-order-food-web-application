from django.shortcuts import render
from django.http import HttpResponse
from .models import Person, Food, Order, Food_Order
from .forms import Order_Form, Date_Form
import copy

# Create your views here.
def index(request):
    #create_test_values()
    #print(Order.objects.all()[1].person)
    persons = Person.objects.all()
    menu = Food.objects.all()
    order_form = Order_Form()
    if request.method == 'GET':
        return render(request, 'index.html', {'persons':persons, 'menu':menu, 'order_form':order_form})
    elif request.method == 'POST':
        #print(request.POST)
        order = Order()
        day = request.POST.get('date_day')
        month = request.POST.get('date_month')
        year = request.POST.get('date_year')
        date = year+'-'+month+'-'+day # YYYY-MM-DD
        order.date = date
        order.person = Person.objects.get(pk=request.POST.get('person'))
        food_amounts = request.POST.getlist('amount')
        # TODO check that at least 1 amount > 0
        order.save()

        if len(menu) == len(food_amounts):
            for i in range(len(food_amounts)):
                food_order = Food_Order()
                food_order.order = order
                food_order.food = menu[i]
                food_order.amount = food_amounts[i]
                if int(food_order.amount) > 0:
                    food_order.save()
            return render(request, 'message.html', {'message':'Ваш заказ принят!'})
        return render(request, 'message.html', {'message':'Что-то пошло не так.'})

def history(request):
    persons = Person.objects.all()
    if request.method == 'GET':
        return render(request, 'history.html', {'persons':persons})
    elif request.method == 'POST':
        person = request.POST.get('person')
        orders = Order.objects.filter(person=person)
        for o in orders:
            foods = Food_Order.objects.filter(order=o)
            o.foods = foods
        return render(request, 'history.html', {'persons':persons, 'person':Person.objects.get(pk=person), 'orders':orders})
            
def report(request):
    date_form = Date_Form()
    if request.method == 'GET':
        return render(request, 'report.html', {'date_form':date_form})
    elif request.method == 'POST':
        day = request.POST.get('date_day')
        month = request.POST.get('date_month')
        year = request.POST.get('date_year')
        date = year+'-'+month+'-'+day # YYYY-MM-DD
        orders = Order.objects.filter(date=date)

        overall_sum = 0
        food_dict = dict()
        
        for order in orders:
            food_orders = Food_Order.objects.filter(order=order)
            for food_order in food_orders:
                food = food_order.food
                amount = food_order.amount
                if food.name not in food_dict.keys():
                    #food_data = object()
                    food_data = copy.copy(food)
                    food_data.amount = 0
                    food_data.name = food.name
                    food_data.price = food.price
                    food_data.sum = 0
                    food_dict[food.name] = food_data
                food_dict[food.name].amount += amount
                food_dict[food.name].sum += amount * food.price
                overall_sum += amount * food.price

        food_list = food_dict.values()
        return render(request, 'report.html', {'date_form':date_form, 'date':date, 'food_list':food_list, 'overall_sum':overall_sum})

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
