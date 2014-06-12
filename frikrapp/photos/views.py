# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from models import Photo, VISIBILITY_PUBLIC
from django.http.response import HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from forms import LoginForm, PhotoForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView
from django.utils.decorators import method_decorator


class HomeView(View):

    def get(self, request):
        """
        Se ejecuta en / y carga la plantilla photos/templates/photos/index.html
        :param request: objeto request
        :return: objeto response
        """
        photo_list = Photo.objects.filter(visibility=VISIBILITY_PUBLIC).order_by('-created_at')
        context = {
            'photos' : photo_list[:3]
        }
        return render(request, 'photos/index.html', context)


class PhotoDetailView(View):

    def get(self, request, pk):
        """
        Muestra el detalle de una foto
        :param request: objeto request
        :param pk: primary key de la foto
        :return: objeto response
        """
        possible_photos = Photo.objects.filter(pk=pk)
        if request.user.is_authenticated():
            possible_photos = possible_photos.filter(Q(owner=request.user) | Q(visibility=VISIBILITY_PUBLIC))
        else:
            possible_photos = possible_photos.filter(visibility=VISIBILITY_PUBLIC)

        if len(possible_photos) == 0:
            return HttpResponseNotFound('No existe la foto seleccionada')
        else:
            context = {
                'photo' : possible_photos[0]
            }
            return render(request, 'photos/photo_detail.html', context)


class UserLoginView(View):

    def get(self, request):
        login_form = LoginForm()
        context = {
            'form' : login_form
        }
        return render(request, 'photos/login.html', context)



    def post(self, request):
        """
        Gestiona el login de un usuario
        :param request: objeto request
        :return: objeto response
        """
        error_messages = []

        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            username = login_form.cleaned_data.get('user_username')
            password = login_form.cleaned_data.get('user_password')

            user = authenticate(username=username, password=password)
            if user is None:
                error_messages.append('Nombre de usuario o contraseña incorrectos')
            else:
                if user.is_active:
                    login(request, user) # crea la sesión de usuario
                    next_url = request.GET.get('next', '/')
                    return redirect(next_url)
                else:
                    error_messages.append('El usuario no está activo')

        context = {
            'form' : login_form,
            'errors' : error_messages
        }
        return render(request, 'photos/login.html', context)


class UserLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('/')


class UserProfileView(View):

    @method_decorator( login_required() ) # forzamos a que el usuario esté autenticado
    def get(self, request):
        """
        Presenta el perfil de un usuario con sus fotos
        :param request: objeto request
        :return: objeto response
        """
        context = {
            'photos' : request.user.photo_set.all()
        }
        return render(request, 'photos/profile.html', context)



@login_required()
def create_photo(request):
    """
    Gestiona la creacion de fotos
    :param request:
    :return:
    """
    new_photo = None
    if request.method == 'POST':
        photo_with_user = Photo(owner=request.user) # creamos foto para el usuario autenticado
        form = PhotoForm(request.POST, instance=photo_with_user)
        if form.is_valid():
            new_photo = form.save()
            form = PhotoForm()
    else:
        form = PhotoForm()
    context = {
        'form' : form,
        'photo' : new_photo
    }
    return render(request, 'photos/create_photo.html', context)



class PhotoListView(ListView):
    model = Photo
    template_name = 'photos/photo_list.html'

    def get_queryset(self):
        return Photo.objects.filter(visibility=VISIBILITY_PUBLIC)


















