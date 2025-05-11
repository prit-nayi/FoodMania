from django import forms
from .models import Restaurant, Menu, Category, Food


# Form for adding a Menu

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['menu_name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['food_name', 'food_price', 'food_type', 'image', 'description']