from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms import formset_factory
from django.conf import settings
from PIL import Image
from django.urls import reverse
from .utils import generate_qr_code
from .models import Pet, PetProfileVisibility, QRCode, PetProfileVisibility
from .forms import EditUserDetailsForm, EditUserEmailForm, PetForm, UserForm, PetProfileVisibilityForm
import os

def home(request):
    return render(request, 'home.html')

def is_admin(user):
    return user.is_superuser

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)
            login(request, user)
            return redirect('add_pet')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_profile')
        else:
            # Invalid login
            pass
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()

            # Generar y guardar el código QR
            qr_code_url = request.build_absolute_uri(reverse('petApp:pet_profile', kwargs={'pet_uuid': str(pet.uuid)}))
            qr_code_img = generate_qr_code(qr_code_url)
            qr_code_path = os.path.join(settings.MEDIA_ROOT, f'qr_codes/{pet.uuid}.png')
            qr_code_img.save(qr_code_path)
            pet.qr_code = f'qr_codes/{pet.uuid}.png'
            pet.save()

            for field_name in PetProfileVisibility.get_default_visible_fields():
                visibility, created = PetProfileVisibility.objects.get_or_create(
                    pet=pet,
                    field_name=field_name,
                    defaults={'visible': True}
                )
                if not created:
                    visibility.visible = True
                    visibility.save()

            return redirect('petApp:pet_profile', pet_uuid=pet.uuid)
    else:
        form = PetForm()
    return render(request, 'petApp/add_pet.html', {'form': form})




def pet_profile(request, pet_uuid):
    try:
        pet = get_object_or_404(Pet, uuid=pet_uuid)
    except Pet.DoesNotExist:
        context = {'error_message': 'No se encontró ninguna mascota con el identificador proporcionado.'}
        return render(request, 'petApp/error_page.html', context)

    visible_fields = PetProfileVisibility.objects.filter(pet=pet, visible=True)
    context = {'pet': pet, 'visible_fields': visible_fields}
    return render(request, 'petApp/pet_profile.html', context)



@user_passes_test(is_admin)
@login_required
def admin_dashboard(request):
    pets = Pet.objects.all()
    owners = User.objects.filter(is_superuser=False)
    context = {'pets': pets, 'owners': owners}
    return render(request, 'admin_dashboard.html', context)

@login_required
def edit_visibility(request, pet_uuid):
    pet = get_object_or_404(Pet, uuid=pet_uuid, owner=request.user)
    if request.method == 'POST':
        # Actualizar las preferencias de visibilidad basadas en los datos del formulario
        for field_name in ['phone', 'address', 'medical_records', ...]:
            visible = request.POST.get(field_name) == 'on'
            pet_visibility, _ = PetProfileVisibility.objects.get_or_create(pet=pet, field_name=field_name)
            pet_visibility.visible = visible
            pet_visibility.save()
        return redirect('petApp:pet_profile', pet_uuid=pet.uuid)
    else:
        visible_fields = PetProfileVisibility.objects.filter(pet=pet)
        context = {'pet': pet, 'visible_fields': visible_fields}
        return render(request, 'petApp/edit_visibility.html', context)


@login_required
def edit_pet_visibility(request, pet_uuid):
    PetProfileVisibilityFormSet = formset_factory(PetProfileVisibilityForm, extra=0)
    pet = get_object_or_404(Pet, uuid=pet_uuid)
    
    if request.method == 'POST':
        formset = PetProfileVisibilityFormSet(request.POST, prefix='visibility')
        if formset.is_valid():
            for form in formset:
                pet_profile_visibility = form.save(commit=False)
                pet_profile_visibility.pet = pet
                existing_visibility = PetProfileVisibility.objects.get(pet=pet, field_name=pet_profile_visibility.field_name)
                existing_visibility.visible = pet_profile_visibility.visible
                existing_visibility.save()
            return redirect('pet_profile', pet_uuid=pet.uuid)
    else:
        queryset = PetProfileVisibility.objects.filter(pet=pet)
        if not queryset.exists():
            default_visible_fields = PetProfileVisibility.get_default_visible_fields()
            initial_data = [{'field_name': field, 'visible': True} for field in default_visible_fields]
        else:
            initial_data = [{'field_name': obj.field_name, 'visible': obj.visible} for obj in queryset]

        formset = PetProfileVisibilityFormSet(initial=initial_data, prefix='visibility')
    
    context = {'formset': formset, 'pet': pet}
    return render(request, 'edit_pet_visibility.html', context)


@login_required
def user_profile(request):
    user = request.user
    pets = Pet.objects.filter(owner=user)
    context = {'user': user, 'pets': pets}
    return render(request, 'user_profile.html', context)

@login_required
def edit_user_email(request):
    user = request.user
    if request.method == 'POST':
        form = EditUserEmailForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Correo electrónico actualizado con éxito')
            return redirect('petApp:user_profile')
    else:
        form = EditUserEmailForm(instance=user)
    return render(request, 'edit_user_email.html', {'form': form})

@login_required
def edit_user_details(request):
    user = request.user
    if request.method == 'POST':
        form = EditUserDetailsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Datos personales actualizados con éxito')
            return redirect('petApp:user_profile')
    else:
        form = EditUserDetailsForm(instance=user)
    return render(request, 'edit_user_details.html', {'form': form})