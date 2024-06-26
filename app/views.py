from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
import json
# Create your views here.
def home(request):
    products = Product.objects.all()
    context= {'products': products}
    return render(request,'app/home.html',context)
def cart(request):
    if request.user.is_authenticated: 
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitems_set.all()
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
    context= {'items':items,'order':order}
    return render(request,'app/cart.html',context)
def checkout(request):
    if request.user.is_authenticated: 
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitems_set.all()
    else:
        items =[]
        order = {'get_cart_items':0,'get_cart_total':0}
    context= {'items':items,'order':order}
    return render(request,'app/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId =  data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, create = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, create = OrderItems.objects.get_or_create(order=order,product=product)
    if action == 'add': 
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
            orderItem.delete()
    return JsonResponse('added',safe=False)

