from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import MinValueValidator,MaxValueValidator
from django.db.models.functions import Lower
class UserManager(BaseUserManager):
    def create_user(self,name,phone_number,password=None):
        if not phone_number:
            raise ValueError('phone number is must')
        user=self.model(phone_number=phone_number,name=name)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,name,phone_number,password):
        user=self.create_user(name=name,phone_number=phone_number,password=password)
        user.is_staff=True
        user.is_superuser=True
        user.save()
        return user
    
class User(AbstractBaseUser):
    name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=12,unique=True,db_index=True)
    created_by=models.DateTimeField(auto_now_add=True)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)


    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['name']
    objects=UserManager()  

    def __str__(self):
        return self.name 
    

class Place(models.Model):
    name=models.CharField(max_length=255,db_index=True)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints=[
        models.UniqueConstraint(
            Lower("name"),
            Lower('address'),
            name="unique_places"
        )
        ]
    def __str__(self):
        return self.name
    
class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviews')
    place=models.ForeignKey(Place,on_delete=models.CASCADE,related_name='reviews')
    rating=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=['user','place'],
                name='one_review_per_user_per_place'
            )
        ]
        ordering=['-created_at']
    def __str__(self):
        return f'review by {self.user.name} for {self.place.name}'     





