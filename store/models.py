from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#our customer model
#its gonna inherit from models.Model
class Customer(models.Model):
    #one customer one user is one to on field
    user = models.OneToOneField(User, on_delete= models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null = True)
    email = models.CharField(max_length=200, null=True)

    #this is the value that will show up in admin panel when we query the model
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null = True)
    seller = models.CharField(max_length=200, null = True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    #to handle error if there is no image
    #property let us access image as an attribute rather than a method
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    #many-to-one relationship customer can have multile orders
    #setnull means if customer get deleted we want to set its value to null
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank= True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    #if complete false means continue adding product if true means order is done    
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            shipping = True
        return shipping
		
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    #get items of the cart
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

#this model gives customer information its address
class ShippingAddress(models.Model):
    #set null as even if the order gets deleted we want to store the shipping address of our customer
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address


