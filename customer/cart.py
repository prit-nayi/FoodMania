# cart.py
from decimal import Decimal
from restaurant.models import Food
class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, food, quantity=1, update_quantity=False):
        """
        Add a food item to the cart or update its quantity.
        """
        food_id = str(food.id)
        if food_id not in self.cart:
            self.cart[food_id] = {'quantity': 0, 'price': str(food.food_price)}
        if update_quantity:
            self.cart[food_id]['quantity'] = quantity
        else:
            self.cart[food_id]['quantity'] += quantity
        self.save()

    def remove(self, food):
        """
        Remove a food item from the cart.
        """
        food_id = str(food.id)
        if food_id in self.cart:
            del self.cart[food_id]
            self.save()

    def save(self):
        """
        Save the cart in the session.
        """
        self.session.modified = True

    def __iter__(self):
        """
        Iterate over the items in the cart and get the food items from the database.
        """
        food_ids = self.cart.keys()
        foods = Food.objects.filter(id__in=food_ids)
        cart = self.cart.copy()
        for food in foods:
            cart[str(food.id)]['food'] = food
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Get the total number of items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculate the total price of all items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Remove all items from the cart.
        """
        del self.session['cart']
        self.save()