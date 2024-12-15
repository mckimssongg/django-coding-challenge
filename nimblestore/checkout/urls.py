from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"products", views.ProductListView, basename="product")

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("api/order/", views.OrderView.as_view(), name="order"),
    path("api/", include(router.urls)),
]
