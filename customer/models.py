# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from restaurant.models import Restaurant , Food


class Customer(models.Model):
    cid = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=100)
    phone_number = models.BigIntegerField(db_column='Phone_number')  # Field name made lowercase.
    email_id = models.CharField(db_column='Email-id', max_length=45, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    address = models.CharField(db_column='Address', max_length=500)  # Field name made lowercase.
    password = models.CharField(max_length=45 , blank=True, null=True)

    class Meta:
        db_table = 'customer'
    
    def  __str__(self): 
        return  (self.cname)




class Order(models.Model):
    oid = models.AutoField(db_column='Oid', primary_key=True)  # Field name made lowercase.
    oname = models.CharField(max_length=800)
    price = models.IntegerField()
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount')  # Field name made lowercase.
    customization = models.CharField(db_column='Customization', max_length=5000, blank=True, null=True)  # Field name made lowercase.
    payment_method = models.CharField(db_column='payment-method', max_length=45)  # Field renamed to remove unsuitable characters.
    booking_date = models.DateField(db_column='Booking-date')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cus_id = models.ForeignKey(Customer, models.DO_NOTHING, db_column='cus_id', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    res_id = models.ForeignKey(Restaurant,on_delete=models.CASCADE, related_name='orders',blank=True, null=True)  # Field renamed to remove unsuitable characters.
    items = models.ManyToManyField( Food, related_name='orders')  # Add a ManyToManyField to store items being ordered

  

    def __int__(self):
        return self.oid





