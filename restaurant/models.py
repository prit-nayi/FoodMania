from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    contact = models.CharField(max_length=15)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    rest_image = models.FileField(upload_to='rest_image/',default='',blank=True, null=True)
    gst_number = models.CharField(max_length=15)
    fssai_number = models.CharField(max_length=20)

    owner_name = models.CharField(max_length=100)
    owner_phone_no = models.CharField(max_length=15)
    owner_email = models.EmailField()
    pan_number = models.CharField(max_length=20)

    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=20)

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    menu_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.menu_name} (Menu for {self.restaurant.name})"

class Category(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='categories')
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category_name} (Category in {self.menu.menu_name})"

class Food(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foods')
    food_name = models.CharField(max_length=100)
    food_price = models.DecimalField(max_digits=10, decimal_places=2)
    FOOD_TYPE_CHOICES = [
        ('VEG', 'Vegetarian'),
        ('NON_VEG', 'Non-Vegetarian'),
    ]
    food_type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES)
    image = models.FileField(upload_to='food_images/',default='',blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.food_name} (Food in {self.category.category_name})"