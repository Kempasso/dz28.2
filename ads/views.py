
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView
from ads.models import Ad, Category

import json

from dz_27 import settings
from users.models import Person


def index(request):
    return JsonResponse({"status": "ok"})


class AdDetailView(DetailView):
    model = Ad

    def get(self, *args, **kwargs):
        """Получение объявления по id"""
        ad = self.get_object()
        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
            "price": ad.price,
            "description": ad.description,
            "image": ad.image.url,
            "is_published": ad.is_published
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        """Получение всех объявлений"""
        super().get(self, request, *args, **kwargs)

        self.object_list = self.object_list.select_related('author', 'category').order_by('-price')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)

        ads = []
        for ad in page_obj:
            image = ad.image.url if ad.image else None
            ads.append({
                "id": ad.pk,
                "name": ad.name,
                "price": ad.price,
                "description": ad.description,
                "image": image,
                "is_published": ad.is_published,
                "author_id": ad.author_id,
                "category_id": ad.category_id
            })

        response = {
            "items": ads,
            "num_page": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'price', 'description', 'image', 'is_published']

    def patch(self, request, *args, **kwargs):
        """Обновление данных объявления"""
        super().post(self, request, *args, **kwargs)

        ad_data = json.loads(request.body)

        self.object.name = ad_data.get('name', self.object.name)
        self.object.price = ad_data.get('price', self.object.price)
        self.object.description = ad_data.get('description', self.object.description)
        self.object.image = ad_data.get('image', self.object.image)
        self.object.is_published = ad_data.get('is_published', self.object.is_published)

        self.object.author = get_object_or_404(Person, pk=ad_data.get('author', self.object.author.pk))
        self.object.category = get_object_or_404(Category, pk=ad_data.get('category', self.object.category.pk))

        self.object.save()

        return JsonResponse({
            "name": self.object.name,
            "price": self.object.price,
            "description": self.object.description,
            "image": self.object.image.url,
            "is_published": self.object.is_published,
            "author": self.object.author_id,
            "category": self.object.category_id
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'price', 'description', 'image', 'is_published', 'author_id', 'category_id']

    def post(self, request, *args, **kwargs):
        """Создание объявления"""
        ad_data = json.loads(request.body)

        new_ad = Ad.objects.create(
            name=ad_data['name'],
            price=ad_data['price'],
            description=ad_data['description'],
            is_published=ad_data['is_published']
        )
        new_ad.image = ad_data.get('image', None)
        new_ad.author = get_object_or_404(Person, pk=ad_data['author'])
        new_ad.category = get_object_or_404(Category, pk=ad_data['category'])

        new_ad.save()
        response = {
            "name": new_ad.name,
            "price": new_ad.price,
            "description": new_ad.description,
            "image": None,
            "is_published": new_ad.is_published,
            "author": new_ad.author_id,
            "category": new_ad.category_id
        }
        if new_ad.image:
            response['image'] = new_ad.image.url
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageLoadView(UpdateView):
    model = Ad
    fields = ['name', 'price', 'description', 'image', 'is_published', 'author_id', 'category_id']

    def post(self, request, *args, **kwargs):
        """Добавление картинки"""
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()
        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
            "image": self.object.image.url
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'  # URL на который перенаправляет пользователя после удаления записи

    def delete(self, request, *args, **kwargs):
        """Удаление объявления"""
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, *args, **kwargs):
        """Получение категории по id"""
        categories = self.get_object()
        return JsonResponse({
            "id": categories.pk,
            "name": categories.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CatListView(View):

    def get(self, request):
        """Получение всех категорий"""

        cat_list = Category.objects.all()
        cat_list = cat_list.order_by('name')
        return JsonResponse([
            {"id": i.pk, "name": i.name}
            for i in cat_list], safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        """Создание категории"""
        cat_data = json.loads(request.body)

        new_cat = Category.objects.create(name=cat_data['name'])
        return JsonResponse({"name": new_cat.name})


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        """Обновление категории"""
        super().post(self, request, *args, **kwargs)

        cat_data = json.loads(request.body)

        self.object.name = cat_data.get('name', self.object.name)
        self.object.save()
        return JsonResponse({"name": self.object.name})


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        """Удаление категории"""
        super().delete(self, request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)

