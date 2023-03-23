import uuid
from django.db import models
from django.contrib.auth.models import User
from secrets import token_hex

class Pet(models.Model):
    DOG = 'dog'
    CAT = 'cat'
    OTHER = 'other'
    SPECIES = [(
        DOG, ('Perro')),
        (CAT, ('Gato')),
        (OTHER, ('Otro')
    )]

    id = models.AutoField(primary_key=True)  # Identificador único creciente
    uuid = models.CharField(max_length=7, unique=True, default=token_hex(3))  # Código alfanumérico único
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='pets/')
    phone = models.CharField(max_length=20, default='+5491123456710')
    address = models.CharField(max_length=255)
    medical_records = models.TextField()
    birth_date = models.CharField(max_length=20, default='01/01/23')
    description = models.CharField(max_length=255,default='Unknown')
    color = models.CharField(max_length=50,default='Unknown')
    breed = models.CharField(max_length=50,default='Unknown')
    qr_code = models.ImageField(upload_to='qr_codes/',blank=True,null=True)
    vet_location = models.CharField(max_length=50)
    species = models.CharField(max_length=20, choices=SPECIES, default=DOG) 
    
    # Agregar campos adicionales según sea necesario


    def save(self, *args, **kwargs):
        while not self.uuid or Pet.objects.filter(uuid=self.uuid).exists():
            self.uuid = token_hex(3)
        super(Pet, self).save(*args, **kwargs)

class PetProfileVisibility(models.Model):
    FIELD_CHOICES = [
        ('name', 'Name'),
        ('birth_date', 'Birth Date'),
        ('breed', 'Breed'),
        ('description', 'Description'),
        ('med_records','Medical Records'),
        ('profile_picture','Profile Picture'),
        ('address','address'),
        ('color','color')
        # Agrega aquí más campos si lo deseas
    ]
    @staticmethod
    def get_default_visible_fields():
        return [[t[0] for t in PetProfileVisibility.FIELD_CHOICES]
        ]

    pet = models.OneToOneField(Pet, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=50, choices=FIELD_CHOICES)
    visible = models.BooleanField(default=True)

    class Meta:
        unique_together = ('pet', 'field_name')

class QRCode(models.Model):
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qrcodes/')
