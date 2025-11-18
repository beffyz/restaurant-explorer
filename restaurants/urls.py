from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.restaurants, name="restaurants"),
    path("<int:id>/", views.restaurant, name="restaurant"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
