from rest_framework import serializers
from .models import User,Place,Review
from django.db.models import Avg
from reviews_api import models

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['name','phone_number']
    def create(self,validated_data):
        user=User.objects.create_user(
            phone_number=validated_data['phone_number'],
            name=validated_data['name']
        )    
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    phone_number=serializers.CharField()  

class ReviewSerializer(serializers.ModelSerializer):
    user_name=serializers.CharField(source="user.name",read_only=True)
    class Meta:
        model=Review
        fields=['id','user_name','rating','text','created_at']

class AddReviewSerializer(serializers.ModelSerializer):
    place_name=serializers.CharField(max_length=255)
    place_address=serializers.CharField()
    rating=serializers.IntegerField(min_value=1,max_value=5)
    text=serializers.CharField()

class PlaceSearchSerialzer(serializers.ModelSerializer):
    average_rating=serializers.FloatField()
    class Meta:
        model=Place
        fields=['id','name','average_rating']
    # def get_average_rating(self,obj):
    #     avg_rating=obj.reviews.aggregate(avg=Avg('rating'))['avg']  
    #     return round(avg_rating,2) if avg_rating else 0  

class PlaceDetailSerialzer(serializers.ModelSerializer):
    average_rating=serializers.SerializerMethodField()
    reviews=serializers.SerializerMethodField()
    class Meta:
        model=Place
        fields=['id', 'name', 'address', 'average_rating', 'reviews']
    def get_average_rating(self,obj):
        avg_rating=obj.reviews.aggregate(avg=Avg('rating'))['avg']  
        return round(avg_rating,2) if avg_rating else 0  
    def get_reviews(self,obj):
        request=self.context.get('request')
        user=request.user if request else None

        reviews=obj.reviews.all()
        if user:
            user_reviews=reviews.filter(user=user)
            other_reviews=reviews.exclude(user=user)
            ordered_reviews=list(user_reviews) + list(other_reviews)
        else:
            ordered_reviews=list(reviews) 
        return ReviewSerializer(ordered_reviews,many=True).data     


