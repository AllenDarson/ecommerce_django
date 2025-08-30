from django.db import models

# Create your models here.
class Product_add(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Manufacturing_date = models.DateField(null=True, blank=True)
    expiry_date = models.CharField(max_length=255)
    # Allow null and blank
    image = models.ImageField(upload_to='photos/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class AdminUsers(models.Model):    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    
class Cart(models.Model):
    buyer_username = models.CharField(max_length=100)  
    product_id = models.IntegerField()
   
    
class Buyer(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    
class Carts(models.Model):
    buyer_name = models.CharField(max_length=100)
    buyer_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    product_id = models.IntegerField()
    
class Vendor(models.Model):
    vendor_name = models.CharField(max_length=100)
    vendor_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    vendor_password = models.CharField(max_length=100, null=True, blank=True)
    product_brought = models.CharField(max_length=255)
    
class Product_vendor(models.Model):
    vendor_id = models.CharField(max_length=50)
    product_id = models.AutoField(primary_key=True)
    product_brand = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    Manufacturing_date = models.DateField(null=True, blank=True)
    expiry_date = models.CharField(max_length=255)
    # Allow null and blank
    image = models.ImageField(upload_to='photos/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    vendor_pwd =models.CharField(max_length=100)
    
class Staff(models.Model):
    staff_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)

class Order(models.Model):
    username = models.CharField(max_length=50)  # store the user's name directly
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)