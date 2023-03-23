from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Pet,PetProfileVisibility
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class PetForm(forms.ModelForm):
    

    name = forms.CharField(label= 'Nombre')
    photo = forms.ImageField(label= 'Elije una foto')
    phone = forms.IntegerField(label= 'Numero de telefono de contacto', widget=forms.NumberInput)
    address = forms.CharField(label= 'Direccion (no es publica)')
    medical_records = forms.CharField(label= 'Ingresa algun dato importante sobre su alimentacion o salud', widget=forms.Textarea)
    birth_date = forms.DateField(label= 'Fecha de Nacimiento', widget=forms.DateInput)
    description = forms.CharField(label= 'Como es tu mascota?', widget=forms.Textarea)
    color = forms.CharField(label= 'De que color es tu mascota')
    breed = forms.CharField(label= 'Que raza es?')
    vet_location = forms.CharField(label= 'Direccion de su veterinario')
    species = forms.ChoiceField(choices=Pet.SPECIES, initial='Perro', label='Especie', required=False, widget=forms.Select)




    class Meta:
        model = Pet
        fields = ('name','species','breed','color', 'birth_date', 'description', 'photo',
                   'phone', 'address', 'vet_location','medical_records')

class PetProfileVisibilityForm(forms.ModelForm):
    class Meta:
        model = PetProfileVisibility
        fields = ('field_name', 'visible',)
        widgets = {
            'field_name': forms.HiddenInput(),
        }

class PetVisibilityForm(forms.ModelForm):
    class Meta:
        model = PetProfileVisibility
        fields = ['field_name', 'visible']

class EditUserEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        labels = {
            'email': 'Correo electrónico',
        }

class EditUserDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }