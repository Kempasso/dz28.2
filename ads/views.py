
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from ads.models import Ads, Categories

import json


def index(request):
    return JsonResponse({"status": "ok"})


class AdsDetailView(DetailView):
    model = Ads

    def get(self, *args, **kwargs):
        """Получение объявления по id"""
        ads = self.get_object()
        return JsonResponse({
            "id": ads.pk,
            "name": ads.name,
            "author": ads.author,
            "price": ads.price,
            "description": ads.description,
            "address": ads.address,
            "is_published": ads.is_published,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsListView(View):

    def get(self, request):
        """Получение всех объявлений"""
        ads_list = Ads.objects.all()
        return JsonResponse([{
            "id": i.pk,
            "name": i.name,
            "author": i.author,
            "price": i.price,
            "description": i.description,
            "address": i.address,
            "is_published": i.is_published,
        } for i in ads_list], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        new_ad = Ads.objects.create(**data)
        return JsonResponse({
            "id": new_ad.pk,
            "name": new_ad.name,
            "author": new_ad.author,
            "price": new_ad.price,
            "description": new_ad.description,
            "address": new_ad.address,
            "is_published": new_ad.is_published,
        })


class CategoryDetailView(DetailView):
    model = Categories

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
        cat_list = Categories.objects.all()
        return JsonResponse([
            {"id": i.pk, "name": i.name}
            for i in cat_list], safe=False)

    def post(self, request):

        data = json.loads(request.body)
        new_cat = Categories.objects.create(**data)
        return JsonResponse({
            "id": new_cat.pk,
            "name": new_cat.name
        })
