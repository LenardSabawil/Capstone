from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from reservation.models import Booking
from .models import Product, Order
from .forms import ProductForm, OrderForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

@login_required
def index(request):
    orders = Order.objects.all()
    products = Product.objects.all()
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()
    products_count = Product.objects.all().count()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.staff = request.user
            instance.save()
        return redirect('dashboard-index')
    else:
        form = OrderForm()
    context = {
        'orders':orders,
        'form': form,
        'products': products,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def staff(request):
    workers = User.objects.all()
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()
    products_count = Product.objects.all().count()
    context = {
        'workers': workers,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
    }
    return render(request, 'dashboard/staff.html', context)

@login_required
def product(request):
    items = Product.objects.all()
    products_count = items.count()
    workers_count = User.objects.all().count()
    orders_count = Order.objects.all().count()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
        return redirect('dashboard-product')
    else:
        form = ProductForm()
    context = {
        'items': items,
        'form': form,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
    }
    return render(request, 'dashboard/product.html', context)


@login_required
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')


@login_required
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
        return redirect('dashboard-product')
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form,
    }
    return render(request, 'dashboard/product_update.html', context)


@login_required
def order(request):
    orders = Order.objects.all()
    orders_count = orders.count()
    workers_count = User.objects.all().count()
    products_count = Product.objects.all().count()
    context = {
        'orders': orders,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
    }
    return render(request, 'dashboard/order.html', context)

@login_required
def reservation_list(request):
    booking = Booking.objects.all()
    orders_count = Order.objects.all().count()
    workers_count = User.objects.all().count()
    products_count = Product.objects.all().count()
    context = {
        'booking': booking,
        'workers_count': workers_count,
        'orders_count': orders_count,
        'products_count': products_count,
    }
    return render(request, 'dashboard/reservation_list.html', context)


def approve_booking(request, pk):
    booking = Booking.objects.all(pk=pk)
    if request.method == "POST":
         if request.POST.get('reject') == None:
            booking.status = "Accepted"
         else: 
            booking.remarks = request.POST.get('reject')
            booking.status = "Rejected"
            booking.save()

    context={
        'booking': booking,
    }
    return render(request, 'dashboard/reservation_list.html', context)


def dashboard(request):
    return render(request, 'costumer_dashboard/index.html')

def reservation(request):
    return render(request, 'costumer_dashboard/reservation.html')

def about(request):
    return render(request, 'costumer_dashboard/about.html')

def contact(request):
    return render(request, 'costumer_dashboard/contact.html')

def rooms(request):
    return render(request, 'costumer_dashboard/rooms.html')

def events(request):
    return render(request, 'costumer_dashboard/events.html')

