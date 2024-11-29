from django.http.response import JsonResponse
from django.views import generic
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import Product
from rest_framework.response import Response
from .serializers import ProductSerializer


class IndexView(generic.TemplateView):
    template_name = "index.html"


class ProductListView(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be listed.
    """
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderView(APIView):
    parser_classes = (JSONParser,)
    authentication_classes = []

    def post(self, request):
        """
        API endpoint que calcula el total de la orden.
        """
        order_items = request.data

        if not isinstance(order_items, list):
            return Response({'error': 'Formato de datos inválido. Se espera una lista de productos.'}, status=400)

        total = 0
        for item in order_items:
            product_name = item.get('product')
            quantity = item.get('quantity')

            if not product_name or quantity is None:
                return Response({'error': 'Cada producto debe tener un nombre y una cantidad.'}, status=400)

            try:
                quantity = int(quantity)
            except ValueError:
                return Response({'error': f'Cantidad inválida para el producto {product_name}.'}, status=400)

            try:
                product = Product.objects.get(name=product_name)
            except Product.DoesNotExist:
                return Response({'error': f'El producto {product_name} no existe.'}, status=404)

            if product.quantity < quantity:
                return Response({'error': f'No hay suficiente cantidad para el producto {product_name}.'}, status=400)

            # Calcula el total
            total += product.price * quantity

            # Actualiza la cantidad del producto
            product.quantity -= quantity
            product.save()

        response_obj = {"total": total}
        return Response(response_obj, status=200)