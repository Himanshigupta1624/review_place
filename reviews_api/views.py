from rest_framework import status,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.models import Token
from django.db.models import Q,Avg,Case,When,IntegerField,Value
from django.db.models.functions import Round,Coalesce
from .models import User,Place,Review
from .serializers import (RegistrationSerializer,LoginSerializer,AddReviewSerializer,PlaceDetailSerialzer,PlaceSearchSerialzer,ReviewSerializer)

class RegisterView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token,created=Token.objects.get_or_create(user=user)
            return Response({
                'token':token.key,
                'user_id':user.id,
                'name':user.name,
                'phone_number':user.phone_number
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number=serializer.validated_data['phone_number']
            try:
                user=User.objects.get(phone_number=phone_number)
                token,created=Token.objects.get_or_create(user=user)
                return Response({
                    'token':token.key,
                    'user_id':user.id,
                    'name':user.name,
                    'phone_number':user.phone_number
                })  
            except User.DoesNotExist:
                return Response({'error':"user doesn't exist"},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class AddReviewView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=AddReviewSerializer(data=request.data)
        if serializer.is_valid():
            place_name=serializer.validated_data['place_name']
            place_address=serializer.validated_data['place_address']
            rating=serializer.validated_data['rating']
            text=serializer.validated_data['text']

            place,created=Place.objects.get_or_create(
                name=place_name,address=place_address

            )
            review=Review.objects.create(
                user=request.user,
                place=place,
                rating=rating,
                text=text
            )
            return Response({
                'id':'review.id',
                'place_id':place.id,
                'place_name':place.name,
                'rating':review.rating,
                'text':review.text,
                'created_at':review.created_at
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   


class PlaceSearchView(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=PlaceSearchSerialzer

    def get_queryset(self):
        queryset=Place.objects.annotate(
            average_rating=Coalesce(Round(Avg('reviews__rating'), 2), Value(0.0)))
        name=self.request.query_params.get('name',None)
        min_rating=self.request.query_params.get('min_rating',None)
        if min_rating:
            try:
                min_rating=float(min_rating)
                queryset=queryset.filter(average_rating__gte=min_rating)
            except ValueError:
                pass
        if name:
            queryset=queryset.filter(Q(name__icontains=name)|Q(name__icontains=name)).annotate(
                match_priority=Case(
                    When(name__iexact=name,then=1),
                    default=2,
                    output_field=IntegerField())
            ).order_by('match_priority','name') 
        else:
            queryset=queryset.order_by('name')
        return queryset
class PlaceDetailView(generics.RetrieveAPIView):
    queryset=Place.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class=PlaceDetailSerialzer

    def get_serializer_context(self):
        context=super().get_serializer_context()
        context['request']=self.request
        return context             



             
