import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import Ad
from dz_27 import settings
from users.models import Person, Location


class UserListView(ListView):
    model = Person

    queryset = Person.objects.annotate(total_ads=Count('ad', filter=Q(ad__is_published=True)))

    def get(self, request, *args, **kwargs):
        """Получение всех пользователей"""
        super().get(self, request, *args, **kwargs)

        self.object_list = self.object_list.prefetch_related('location').order_by("username")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_num = request.GET.get('page') if request.GET.get('page') else 1
        page_obj = paginator.get_page(page_num)

        users = []
        for user in page_obj:
            users.append({
                "id": user.pk,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "password": user.password,
                "role": user.role,
                "age": user.age,
                "location": list(map(str, user.location.all())),
                "total_ads": user.total_ads
            })

        response = {
            "items": users,
            "num_page": page_num,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = Person

    def get(self, request, *args, **kwargs):
        """Получение пользователя по id"""
        super().get(self, request, *args, **kwargs)

        user = self.get_object()
        return JsonResponse({
            "id": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "password": user.password,
            "role": user.role,
            "age": user.age,
            "location": list(map(str, user.location.all()))
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = Person
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location"]

    def post(self, request, *args, **kwargs):
        """Создание пользователя"""
        super().post(self, request, *args, **kwargs)

        user_data = json.loads(request.body)

        new_user = Person.objects.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
            password=user_data['password'],
            role=user_data['role'],
            age=user_data['age']
        )

        for location in user_data['location']:
            loc_obj, create = Location.objects.get_or_create(name=location, defaults={'lat': None,
                                                                                      'lng': None})
            new_user.location.add(loc_obj)

        new_user.save()

        return JsonResponse({
            "id": new_user.pk,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "username": new_user.username,
            "password": new_user.password,
            "role": new_user.role,
            "age": new_user.age,
            "location": list(map(str, new_user.location.all()))
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = Person
    fields = ["first_name", "last_name", "username", "password", "role", "age", "location"]

    def patch(self, request, *args, **kwargs):
        """Обновление данных пользователя"""
        super().post(self, request, *args, **kwargs)

        user_data = json.loads(request.body)

        self.object.first_name = user_data.get('first_name', self.object.first_name)
        self.object.last_name = user_data.get('last_name', self.object.last_name)
        self.object.username = user_data.get('username', self.object.username)
        self.object.password = user_data.get('password', self.object.password)
        self.object.role = user_data.get('role', self.object.role)
        self.object.age = user_data.get('age', self.object.age)
        self.object.age = user_data.get('age', self.object.age)

        if user_data.get('location'):
            for location in user_data['location']:
                loc_obj, create = Location.objects.get_or_create(name=location, defaults={'lat': None,
                                                                                          'lng': None})
                self.object.location.add(loc_obj)
        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "password": self.object.password,
            "role": self.object.role,
            "age": self.object.age,
            "location": list(map(str, self.object.location.all()))
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = Person
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        """Удаление пользователя"""
        super().delete(self, request, *args, **kwargs)
        return JsonResponse({"status": "ok"})



