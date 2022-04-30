from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    """
        Inherits from default User of Django and extends the fields.
        The following fields are part of Django User Model:
        | id
        | password
        | last_login
        | is_superuser
        | username
        | first_name
        | last_name
        | email
        | is_staff
        | is_active
        | date_joined
        """
    CHOICES = (("seller", "seller"),("buyer", "buyer"),)
    Role=models.CharField(max_length=100,choices=CHOICES,blank=True,null=True)
    Address=models.CharField(max_length=100,blank=True,null=True)
    

    def __str__(self):
        return self.email
class catagory(models.Model):
    name=models.CharField(max_length=50,blank=True)
    def __str__(self) -> str:
        return str(self.id)
class SubCatagory(models.Model):
    main_catagory=models.ForeignKey(catagory,on_delete=models.CASCADE)
    name=models.CharField(max_length=50,blank=True)
    def __str__(self) -> str:
        return str(self.id)
class cover(models.Model):
    catagory=models.ForeignKey(catagory,on_delete=models.CASCADE)
    sub_catagory=models.ForeignKey(SubCatagory,on_delete=models.CASCADE)
    cover=models.ImageField(blank=True, null=True) 
    description=models.CharField(max_length=500,blank=True)
    quantity=models.IntegerField()
    def __str__(self) -> str:
        return str(self.id)
class filedata(models.Model):
    product_cover=models.ForeignKey(cover,on_delete=models.CASCADE)
    Images=models.ImageField(blank=True, null=True) 





    
    

