from django.db import models

# Create your models here.


class Niche(models.Model):
    niche_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.niche_name

class Profile(models.Model):
    name = models.CharField(max_length=100)
    niche = models.ForeignKey(Niche, on_delete=models.CASCADE, null=True, blank=True)
    fee_paid = models.BooleanField(default=False)
    joining_date = models.DateTimeField(auto_now_add=False)
    username = models.CharField(max_length=100)
    email = models.EmailField(blank=False, null=False)
    user_subscription_record = models.BooleanField(default=False)
    p1 = models.BooleanField(default=False, blank=True, null=True)
    p2 = models.BooleanField(default=False, blank=True, null=True)
    p3 = models.BooleanField(default=False, blank=True, null=True)
    def __str__(self):
        return self.name
    
class Products(models.Model):
    product_image = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    niche = models.ForeignKey(Niche, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=False)
    purchase_cost = models.IntegerField(default=0)
    selling_cost = models.IntegerField(default=0)
    profit = models.IntegerField(default=0)
    aliexpress_link = models.URLField(default = "www.elitedrops.net/no_link/")
    alibab_link = models.URLField(default = "www.elitedrops.net/no_link/")
    country = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    age_range = models.CharField(max_length=100)
    audiance = models.CharField(max_length=100)
    intrests = models.CharField(max_length=100, blank=True, null=True)
    approximate_CPA = models.CharField(max_length=100)
    saturation = models.CharField(max_length=100)
    fb_ads = models.URLField(default = "www.elitedrops.net/no_link/")
    videos = models.URLField(default = "www.elitedrops.net/no_link/")
    stores_selling_it = models.URLField(default = "www.elitedrops.net/no_link/")

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=False)
    email = models.EmailField(blank=False, null=False)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return self.name
    

class Service_Offer_Request(models.Model):
    email = models.CharField(max_length=50)
    service = models.CharField(max_length=20)
    message = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.email  