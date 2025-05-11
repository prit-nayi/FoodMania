from django.shortcuts import render , get_object_or_404 ,redirect
from .models import Customer , Order
from django.contrib import messages
from django.contrib.auth.models import User  # Default User model
from django.contrib.auth.hashers import make_password  # For password hashing
from restaurant.models import Restaurant, Menu, Category, Food
from django.views.decorators.http import require_POST
from .cart import Cart
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.

def index(request):

    popular_restaurants = Restaurant.objects.all()[:7]
    restaurants = Restaurant.objects.all()

    context = {
        'restaurants': restaurants,
        'pop_res': popular_restaurants,
    }
    return render(request, 'index.html', context)

def food_detail(request, food_id):
    food = Food.objects.get(id=food_id)
    return render(request, 'food_detail.html', {'food': food})

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menus = restaurant.menus.all()  # Fetch all menus related to the restaurant
    food_items = []
    for menu in menus:
        for category in menu.categories.all():
            food_items.extend(category.foods.all())

    return render(request, 'restaurant_detail.html', {
        'restaurant': restaurant,
        'menus': menus,
        'food_items': food_items,
    })

def login(request):
    if request.method == 'POST':
        username =request.POST['name']
        email =request.POST['email']
        phone =request.POST['ph']
        address =request.POST['add']
        password =request.POST['psw']

        user_data = Customer(cname=username,phone_number=phone,email_id=email,address=address,password=password)
        user_data.save()

        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # Hash the password for security
        )
        return render(request,'login.html')
    return render(request,'login.html')
def signup(request):

    return render(request,'signup.html')

def logout(request):
    request.session.clear()
    return render(request,'login.html')
    

def profile(request):
    # Check if the user is already logged in
    if request.session.get('login'):
        customer_id = request.session.get('customer_id')
        try:
            customer = Customer.objects.get(cid=customer_id)
            context = {'customer': customer}
            return render(request, 'profile.html', context)
        except Customer.DoesNotExist:
            messages.error(request, 'Customer not found.')
            return redirect('login')

    context = {}

    if request.method == 'POST':
        uname = request.POST['name']
        password = request.POST['psw'] 
        try:
            user = User.objects.get(username=uname)
            if user.check_password(password):
                customer = Customer.objects.get(cname=uname)
                request.session['customer_id'] = customer.cid
                request.session['customer_name'] = customer.cname
                request.session['customer_email'] = customer.email_id
                request.session['customer_phone'] = customer.phone_number
                request.session['customer_address'] = customer.address
                request.session['login'] = True
                context = {'customer': customer}
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')
        except (User.DoesNotExist, Customer.DoesNotExist):
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'profile.html', context)

def aboutus(request):
    
    return render(request,'aboutus.html')

@require_POST
def cart_add(request, food_id):
    cart = Cart(request) 
    food = Food.objects.get(id=food_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(food, quantity)
    return redirect('cart_detail')

@require_POST
def cart_remove(request, food_id):
    """
    Remove a food item from the cart.
    """
    cart = Cart(request)
    food = get_object_or_404(Food, id=food_id)
    cart.remove(food)
    return redirect('cart_detail')



def cart_detail(request):
    cart = Cart(request)
    # Assuming the cart contains at least one item
    if cart:
        # Get the restaurant from the first item in the cart
        first_item = next(iter(cart))
        restaurant = first_item['food'].category.menu.restaurant
    else:
        # If the cart is empty, set restaurant to None or a default value
        restaurant = None

    return render(request, 'cart/detail.html', {'cart': cart, 'restaurant': restaurant})


def payment(request):
    # Get the cart from the session
    cart = Cart(request)
    
    # Check if the customer is logged in
    if 'customer_name' not in request.session:
        messages.error(request, 'You need to log in to place an order.')
        return redirect('login')
        
    custname = request.session['customer_name']
    cust = Customer.objects.get(cname=custname)
    # Get today's date for the order date input field
    today = timezone.now().date()

    # Pass the cart and today's date to the template
    context = {
        'cart': cart,
        'today': today,
        'cust': cust
    }
    return render(request, 'payment.html', context)

@require_POST
def process_payment(request):
    cart = Cart(request)
    if not cart:
        return redirect('cart_detail')  # Redirect if the cart is empty

    # Get form data
    customization = request.POST.get('customization', '')
    booking_date_str = request.POST.get('booking_date', '')
    delivery_address = request.POST.get('delivery-address')
    if booking_date_str:
        try:
            booking_date = timezone.datetime.strptime(booking_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format. It must be in YYYY-MM-DD format.')
            return redirect('payment')
    else:
        booking_date = timezone.now().date()
    payment_method = request.POST.get('payment_method')

    # Calculate total amount
    total_amount = cart.get_total_price()

    # Get the customer and restaurant (for simplicity, assume they are available in the session)
    customer_id = request.session.get('customer_id')  # Assuming customer ID is stored in the session
    # Get the restaurant ID from the first item in the cart
    
    first_item = next(iter(cart))
    restaurant_id = first_item['food'].category.menu.restaurant.id  # Assuming restaurant ID is stored in the session

    # Ensure customer and restaurant exist
    try:
        customer = Customer.objects.get(cid=customer_id)
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except (Customer.DoesNotExist, Restaurant.DoesNotExist):
        messages.error(request, 'Invalid customer or restaurant.')
        return redirect('cart_detail')

    # Create the order
    order = Order.objects.create(
        oname="Order from Cart",  # You can customize this based on your requirements
        price=total_amount,
        quantity=sum(item['quantity'] for item in cart),
        amount=total_amount,
        customization=customization,
        payment_method=payment_method,
        booking_date=booking_date,
        cus_id = customer,
        res_id=restaurant,
    )
    order.items.set([item['food'] for item in cart])  # Use set() to assign the many-to-many relationship

    # Clear the cart
    cart.clear()
    global customer_delivery_address
    request.session['delivery_address'] = delivery_address
    customer_delivery_address = {
        'address' : delivery_address
    }
    
    # Redirect to a success page
    return redirect('order_success', order_id=order.oid )

def order_success(request, order_id):
    # Get the order details
    order = get_object_or_404(Order, oid=order_id)
    add = customer_delivery_address['address']
    # Pass the order details to the template
    context = {
        'order': order,
        'address' : add
    }
    return render(request, 'order_success.html', context)


def download_bill(request, order_id):
    # Fetch the order
    order = Order.objects.get(oid=order_id)

    items_with_totals = []
    for item in order.items.all():
        total_price = item.food_price * order.quantity
        items_with_totals.append({
            'food_name': item.food_name,
            'quantity': order.quantity,
            'food_price': item.food_price,
            'total_price': total_price,
        })

    # Render the HTML template
    add = request.session['delivery_address']
    html_string = render_to_string('bill.html', {'order': order , 'address' : add , 'items_with_totals': items_with_totals,})

    response = HttpResponse(html_string, content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="bill_order_{order.oid}.html"'
    return response