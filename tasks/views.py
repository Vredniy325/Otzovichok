from django.db.models.base import Model
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.views import LogoutView
from .models import Otzyv,Rating
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

def Main(request):
    otzyv = Otzyv.objects.all()
    return render(request, "Main.html", {"otzyv": otzyv})

def Register(request):
  return render(request, "Register.html", {})

def Help(request):
  return render(request, "Help.html", {})

def AddOtzyv(request): 
  return render(request, "AddOtzyv.html", {})

def LogIn(request):
  return render(request, "LogIn.html", {})

def Registration(request):
    if request.method == 'POST':
        print("Метод запроса POST")
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        # Проверка паролей на совпадение
        if password != confirmPassword:
            print("Пароли не совпадают")
            return render(request, 'Register.html', {'error': 'Пароли не совпадают'})

        # Проверка наличия пользователя с таким email
        if User.objects.filter(email=email).exists():
            print("Пользователь с таким email уже зарегистрирован")
            return render(request, 'Register.html', {'error': 'Пользователь с таким email уже зарегистрирован'})

        # Создание пользователя
        hashed_password = make_password(password)
        user = User.objects.create(username=username, email=email, password=hashed_password)
        user.save()

        # Перенаправление на главную страницу после успешной регистрации
        return redirect('Main')  

    else:
        print("Метод запроса не POST")
        return render(request, 'Register.html')



def LogInFunc(request):
    if request.method == 'POST':
        print("Метод запроса POST")
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Password:", password)
        print("username:", username)
        # Аутентификация пользователя
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            # Если пользователь существует, выполнить вход
            print("Есть такой молодой человек")
            login(request, user)
            return redirect('Main')  # Перенаправление на главную страницу после входа
        else:
            print("Нет такого человека")
            # Если пользователь не найден, отобразить сообщение об ошибке
            return render(request, 'LogIn.html', {'error': 'Неправильное имя пользователя или пароль'})
    else:
        return render(request, 'LogIn.html')


class UserLogoutView(LogoutView):
    """
    Выход с сайта
    """

def get_client_ip(request):
    """
    Get user's IP
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get(
        'REMOTE_ADDR')
    return ip

class RatingCreateView(generic.View):
    model = Rating

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        otzyv_id = request.POST.get('otzyv_id')
        value_str = request.POST.get('value')
        if value_str == 'NaN':
            return JsonResponse({'error': 'Invalid value for rating'}, status=400)
        try:
            value = int(value_str)
        except ValueError:
            return JsonResponse({'error': 'Invalid value format for rating'},
                                status=400)

        ip_address = get_client_ip(request)
        user = request.user if request.user.is_authenticated else None

        rating, created = self.model.objects.get_or_create(
            otzyv_id=otzyv_id,
            ip_address=ip_address,
            defaults={
                'value': value,
                'user': user
            },
        )
        if not created:
            if rating.value == value:
                rating.delete()
                return JsonResponse({
                    'status': 'deleted',
                    'rating_sum': rating.otzyv.get_sum_rating()
                })
            else:
                rating.value = value
                rating.user = user
                rating.save()
                return JsonResponse({
                    'status': 'updated',
                    'rating_sum': rating.otzyv.get_sum_rating()
                })
        return JsonResponse({
            'status': 'created',
            'rating_sum': rating.otzyv.get_sum_rating()
        })


@csrf_exempt
def UploatRating(request):
    if request.method == 'POST':
        otzyv_id = request.POST.get('otzyv_id')
        try:
            rating = Rating.objects.filter(otzyv_id=otzyv_id)[0]
        except ObjectDoesNotExist:
            print(otzyv_id)
        except IndexError:
            return JsonResponse({'rating': 0,
                                    'message': 'Рейтинг обнавлен'})
        return JsonResponse({'rating': rating.otzyv.get_sum_rating(),
                             'message': 'Рейтинг обнавлен'})

    return JsonResponse({'message': 'Ошибка в обнавлении рейтинга'},
                        status=400)
