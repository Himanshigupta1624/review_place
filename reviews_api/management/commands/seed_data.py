from django.core.management.base import BaseCommand
from reviews_api.models import User, Place, Review
from faker import Faker
import random

fake=Faker()

class Command(BaseCommand):
    help='populate the database with sample data'
    def handle(self,*args,**kwargs):
        self.stdout.write('populating database with sample data...')
        users=[]

        for i in range(10):
            user=User.objects.create_user(
                name=fake.name(),
                phone_number=fake.unique.numerify(text='##########'),

            )
            users.append(user)
        self.stdout.write('created users')   
        self.stdout.write('creating places')
        place_type=['Restaurant', 'Cafe', 'Shop', 'Clinic', 'Pharmacy',
            'Gym', 'Salon', 'Bakery', 'Bar', 'Store'] 
        places=[]
        for i in range(30):
            place_type=random.choice(place_type)
            name=f"{fake.company()} {place_type}"
            address=fake.address().replace("\n",", ")
            place=Place.objects.create( name=name,address=address)
            places.append(place)
        self.stdout.write('created places')
        self.stdout.write('creating reviews')
        reviews_count=0
        for place in places:
            num_reviews=random.randint(1,15)
            reviewed_users = random.sample(users, min(num_reviews, len(users)))
            
            for user in reviewed_users:
                rating=random.choices(
                    [1, 2, 3, 4, 5],
                    weights=[5, 10, 20, 30, 35]
                )[0]
                
                Review.objects.create(
                    user=user,
                    place=place,
                    rating=rating,
                    text=fake.text(max_nb_chars=200)
                )
                reviews_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully populated database with:\n'
            f'  - {len(users)} users\n'
            f'  - {len(places)} places\n'
            f'  - {reviews_count} reviews'
        ))


