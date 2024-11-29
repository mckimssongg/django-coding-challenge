from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/products', views.ProductListView, basename='product')

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("api", views.IndexView.as_view(), name="index"),
    path("api/order/", views.OrderView.as_view(), name="order"),
    path("", include(router.urls)),
]
