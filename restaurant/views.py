from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Restaurant, Menu, Category, Food
from .forms import  MenuForm, CategoryForm, FoodItemForm
from customer.models import Order

# Create your views here.

def registration(request):
    return render(request,'restaurant/register.html')

def rest_login(request):
    if request.method == 'POST':
        print(request.POST)  # Debug: Print all submitted data
        restaurant_name = request.POST.get('restaurant_name')
        print(f"Restaurant Name: {restaurant_name}")

        restaurant_name = request.POST.get('restaurant_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        image = request.POST.get('rimage')
        opening_time = request.POST.get('opentimes')
        closing_time = request.POST.get('closetimes')
        gst_number = request.POST.get('gst')
        fssai_number = request.POST.get('fssai')

        owner_name = request.POST.get('owner_name')
        owner_phone_no = request.POST.get('owner_phone')
        owner_email = request.POST.get('owner_email')
        pan_number = request.POST.get('pan')
        
        bank_name = request.POST.get('bank_name')
        account_number = request.POST.get('account_number')
        ifsc_code = request.POST.get('ifsc_code')

        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Create and save the Restaurant object
        restaurant = Restaurant(
            name=restaurant_name,
            email=email,
            address=address,
            contact=contact,
            rest_image = image,
            opening_time=opening_time,
            closing_time=closing_time,
            gst_number=gst_number,
            fssai_number=fssai_number,
            owner_name=owner_name,
            owner_phone_no=owner_phone_no,
            owner_email=owner_email,
            pan_number=pan_number,
            bank_name=bank_name,
            account_number=account_number,
            ifsc_code=ifsc_code,
            username=username,
            password=password
        )
        restaurant.save()
        
    return render(request,'restaurant/rest_login.html')


def dashboard(request):
    if request.method == 'POST':
        # Retrieve username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username exists in the database
        try:
            restaurant = Restaurant.objects.get(username=username)
        except Restaurant.DoesNotExist:
            # If the username does not exist, show an error message
            messages.error(request, 'Invalid username or password.')
            return redirect('rest_login')

        # Verify the password
        if restaurant.password == password:  # Direct comparison (not secure for production)
            # Log the user in (store the restaurant ID in the session)
            request.session['restaurant_id'] = restaurant.id
            request.session['username'] = restaurant.username
            return redirect('dashboard')
        else:
            # If the password is incorrect, show an error message
            messages.error(request, 'Invalid username or password.')
            return redirect('rest_login')

    # Render the login page for GET requests
    if 'restaurant_id' not in request.session:
        return redirect('rest_login')  # Redirect to login if not logged in

    # Retrieve the logged-in restaurant
    restaurant_id = request.session['restaurant_id']
    restaurant = Restaurant.objects.get(id=restaurant_id)

    # Render the dashboard with restaurant data
    # Store the restaurant directory globally
    global restaurant_directory
    restaurant_directory = {
        'name': restaurant.name,
        'email': restaurant.email,
        'address': restaurant.address,
        'contact': restaurant.contact,
        'rest_image': restaurant.rest_image,
        'opening_time': restaurant.opening_time,
        'closing_time': restaurant.closing_time,
        'gst_number': restaurant.gst_number,
        'fssai_number': restaurant.fssai_number,
        'owner_name': restaurant.owner_name,
        'owner_phone_no': restaurant.owner_phone_no,
        'owner_email': restaurant.owner_email,
        'pan_number': restaurant.pan_number,
        'username': restaurant.username,
        'password': restaurant.password
    }
    orders = Order.objects.filter(res_id=restaurant_id)
    # Retrieve the menu for the current restaurant
    menu = Menu.objects.filter(restaurant=restaurant)

    # Pass the menu to the context
    context = {
        'restaurant': restaurant,
        'orders': orders,
        'menu': menu,
    }
    return render(request, 'restaurant/dashboard.html', context)

def menu(request):
    if request.method == 'POST':
        restaurant_id = request.session.get('restaurant_id')
        if not restaurant_id:
            return redirect('rest_login')  # Redirect to login if not logged in

        restaurant = Restaurant.objects.get(id=restaurant_id)
        menu_name = request.POST.get('menu-name')
        menu = Menu.objects.create(menu_name=menu_name, restaurant=restaurant)

        category_names = request.POST.getlist('category-name')
        for category_index, category_name in enumerate(category_names, start=1):
            category = Category.objects.create(menu=menu, category_name=category_name)

            food_names = request.POST.getlist(f'food-name-{category_index}')
            food_prices = request.POST.getlist(f'food-price-{category_index}')
            food_types = request.POST.getlist(f'food-type-{category_index}')
            food_images = request.FILES.getlist(f'food-image-{category_index}')
            food_descriptions = request.POST.getlist(f'food-description-{category_index}')

            for food_name, food_price, food_type, food_image, food_description in zip(food_names, food_prices, food_types, food_images, food_descriptions):
                Food.objects.create(
                    category=category,
                    food_name=food_name,
                    food_price=food_price,
                    food_type=food_type,
                    image=food_image,
                    description=food_description
                )

    return render(request,'restaurant/menu.html')

def rest_profile(request):
    if 'restaurant_id' not in request.session:
        return redirect('rest_login')  # Redirect to login if not logged in

    # Retrieve the logged-in restaurant
    restaurant_id = request.session['restaurant_id']
    restaurant = Restaurant.objects.get(id=restaurant_id)

    # Use the global restaurant directory
    global restaurant_directory
    restaurant_directory = {
        'name': restaurant.name,
        'email': restaurant.email,
        'address': restaurant.address,
        'contact': restaurant.contact,
        'rest_image' : restaurant.rest_image,
        'opening_time': restaurant.opening_time,
        'closing_time': restaurant.closing_time,
        'gst_number': restaurant.gst_number,
        'fssai_number': restaurant.fssai_number,
        'owner_name': restaurant.owner_name,
        'owner_phone_no': restaurant.owner_phone_no,
        'owner_email': restaurant.owner_email,
        'pan_number': restaurant.pan_number,
        'username': restaurant.username,
        'password': restaurant.password
    }
    menu = Menu.objects.filter(restaurant=restaurant)
    context = {
        'restaurant': restaurant,
        'menu': menu,
    }

    return render(request,'restaurant/rest_profile.html' ,context)

def rest_logout(request):
    if 'restaurant_id' in request.session:
        request.session.flush()
    return redirect('rest_login')


def restaurant_orders(request):
    # Ensure the restaurant is logged in
    if 'restaurant_id' not in request.session:
        return redirect('rest_login')  # Redirect to login if not logged in

    # Get the logged-in restaurant
    restaurant_id = request.session['restaurant_id']
    restaurant = Restaurant.objects.get(id=restaurant_id)

    # Fetch all orders for this restaurant
    orders = Order.objects.filter(res_id=restaurant_id)
# Fetch all items for the orders
    order_items = []
    for order in orders:
        items = order.items.all()  # Assuming there is a related name 'items' for order items
        order_items.extend(items)
    # Pass the orders to the template
    context = {
        'restaurant': restaurant,
        'orders': orders,
        'order_items': order_items

    }
    return render(request, 'restaurant/restaurant_orders.html', context)

