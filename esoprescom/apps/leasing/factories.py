import factory
from django.contrib.auth import get_user_model
import random
from decimal import Decimal
from datetime  import timezone,timedelta,datetime
from django.contrib.auth.models import User
import random
from .models import Clientleasing, Listeimprimante

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.Sequence(lambda n: 'user%d@example.com' % n)
    password = factory.PostGenerationMethodCall('set_password', 'password')

users = User.objects.all()
################# Client Lieasing
class ClientleasingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clientleasing

    nom = factory.Faker('company')
    adresse = factory.Faker('address')
    contact = factory.Faker('name')
    localite = factory.Faker('city')
    refcontrat = factory.Faker('isbn13')
    email = factory.Faker('email')
    date = factory.Faker('date_this_decade', before_today=True, after_today=False)
    userLog = random.choice(users) #factory.SubFactory(UserFactory)


################# Imprimante leasing
class ListeimprimanteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Listeimprimante

    SN = factory.Faker('ean13')
    reference = factory.Faker('word')
    designation = factory.Faker('word')
    description = factory.Faker('text')
    date_acquisition = factory.Faker('date_this_decade', before_today=True, after_today=False)
    garantie = factory.Faker('random_int', min=1, max=3)
    endoflife = factory.Faker('date_this_decade', before_today=False, after_today=True)
    userLog = random.choice(users)  #factory.SubFactory(UserFactory)








