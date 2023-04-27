from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import Product, Collection, OrderItem, Review, Cart, CartItem, Customer, Order
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer,\
        CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer, \
            OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermission


# Create your views here.
# def product_list(request):
#     return HttpResponse("OK harish")

#Creating API views:
# @api_view(['GET','POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={'request':request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)#Deserializing object
#         #Data validation: 1st method
#         # if serializer.is_valid():
#         #     serializer.validated_data
#         #     return Response('ok')
#         # else:
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         #Data validation: 2nd method
#         serializer.is_valid(raise_exception=True)
#         serializer.save() #saving objects (new or updated)
#         # print(serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#Creating Class based Views:
# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={'request':request})
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#implementing Generic Views:
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     #mathiko athawa talako method haru use garne ho
#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()
    
#     # def get_serializer_class(self):
#     #     return ProductSerializer
    
#     def get_serializer_context(self):
#         return {'request':self.request}


# serializing objects
# @api_view()
# def product_detail(request, id):
#     try:
#         product = Product.objects.get(pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)


# serializing objects 2nd way using django shortcut for 404
# @api_view(['GET','PUT','DELETE'])
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         # if product.orderitem_set.count() > 0:
#         if product.orderitems.count() > 0:  #related name in order item
#             return Response({'error': 'Product cannot be deleted as it is associated with an orderitem.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# class ProductDetail(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted as it is associated with an orderitem.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#implementing Generic View for Product detail
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def delete(self, request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         if product.orderitems.count() > 0:
#             return Response({'error': 'Product cannot be deleted as it is associated with an orderitem.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#NOTE: Implementing ProductViewset combining the ProductList and ProductDetail Classes:
class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id', 'unit_price']
    filterset_class = ProductFilter
    # pagination_class=PageNumberPagination
    pagination_class=DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']


    #implementing simple filtering
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get( 'collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)#implementing Filetering
    #     return queryset

    def get_serializer_context(self):
        return {'request':self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
             return Response({'error': 'Product cannot be deleted as it is associated with an orderitem.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)



# @api_view(['GET','POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(queryset, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#implementing Generic View for COllection List
# class CollectionList(ListCreateAPIView):
#     # def get_queryset(self):
#     #     return Collection.objects.annotate(products_count=Count('products')).all()

#     queryset=Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer



# @api_view(['GET','PUT', 'DELETE'])
# def collection_detail(request, pk):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')) ,pk = pk)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if collection.products.count() > 0:
#             return Response({'error':'Collection cannot be deleted as it includes one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products'))
#     serializer_class = CollectionSerializer

#     def delete(self, request, pk):
#         collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')) ,pk = pk)
#         if collection.products.count() > 0:
#             return Response({'error':'Collection cannot be deleted as it includes one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         collection.delete()         
#         return Response(status=status.HTTP_204_NO_CONTENT)


#NOTE: Implementing COllectinVIewSet combining COllectionDetail and COllection List:
class CollectionViewSet(ModelViewSet):
    queryset=Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    def destroy(self, request, *args, **kwargs):
        if Collection.objects.filter(id = kwargs['pk']).count() > 0:
            return Response({'error':'Collection cannot be deleted as it includes one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')) ,pk = pk)
    #     if collection.products.count() > 0:
    #         return Response({'error':'Collection cannot be deleted as it includes one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()         
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(ModelViewSet):
   
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id':self.kwargs['product_pk']}


class CartViewSet(
    CreateModelMixin, 
    RetrieveModelMixin,
    DestroyModelMixin,
    GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class=CartSerializer

    # def get_serializer_context(self):
    #     return {'cart_id': self.kwargs['cart_pk']}


class CartItemsViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
             return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id':self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects\
        .filter(cart_id=self.kwargs['cart_pk']) \
        .select_related('product')

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes =[IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response("ok   ")

    @action(detail=False, methods=['GET','PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id = request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    # queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    # permission_classes=[IsAuthenticated]
    http_method_names = ['get','post', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context = {'user_id':self.request.user.id}    
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer

    #passing user id using context object
    # def get_serializer_context(self):
    #     return {'user_id':self.request.user.id}

    #Applying permissions:
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        
        customer_id = Customer.objects.only('id').get(user_id = user.id)
        return Order.objects.filter(customer_id = customer_id)