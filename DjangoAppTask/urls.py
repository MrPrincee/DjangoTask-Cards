from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cards.views import CardViewSet

router = DefaultRouter()

router.register("cards", CardViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(router.urls),name="cards_api"),

    path("user/auth", include("rest_framework.urls")),

]