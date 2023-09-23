from django.db.models import Q, ExpressionWrapper
from rest_framework import permissions, filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from core.models import User
from courses.models import Product, ProductAccess, ProductLesson, Lesson, LessonView
from courses.serializers import ProductSerializer, ProductAccessSerializer, LessonSerializer, ProductLessonSerializer, \
    LessonViewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum, FloatField, F, Case, When, Value, BooleanField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions




class ProductCreateView(CreateAPIView):
    """Представление для создания продукта.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer

class ProductListView(ListAPIView):
    """Представление для просмотра списка продукта.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ['name']
    ordering_fields = ["name", "created"]
    ordering = ["name"]
    search_fields = ["name"]

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(owner=user, is_deleted=False)


class ProductView(RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления категории цели."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(owner=user)


class ProductAccessCreateView(CreateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductAccessSerializer


class ProductAccessListView(ListAPIView):
    """Представление для просмотра списка доступов к продуктам."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductAccessSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ['user']
    ordering_fields = ["product", "created"]
    ordering = ["product"]
    search_fields = ["product"]

    def get_queryset(self):
        user = self.request.user
        return ProductAccess.objects.filter(user=user)


class ProductAccessView(RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления доступа к продукту."""
    serializer_class = ProductAccessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ProductAccess.objects.filter(user=user)


class LessonCreateView(CreateAPIView):
    """Представление для создания уроков."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LessonSerializer


class LessonListView(ListAPIView):
    """Представление для просмотра списка уроков."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LessonSerializer
    pagination_class = LimitOffsetPagination
    filterset_fields = ['productlesson__product__productaccess__user', 'title']
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ['title']
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        user = self.request.user
        lessons = Lesson.objects.filter(productlesson__product__productaccess__user=user).distinct()
        return lessons


class ProductLessonView(RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления уроков."""
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Lesson.objects.filter(productlesson__product__productaccess__user=user).distinct()


class ProductLessonCreateView(CreateAPIView):
    """Представление для создания связи между продуктом и уроком."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductLessonSerializer


class ProductLessonListView(ListAPIView):
    """Представление для просмотра списка уроков, связанных с продуктами, к которым у пользователя есть доступ."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductLessonSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        accessible_products = ProductAccess.objects.filter(user=user).values_list('product', flat=True)
        return ProductLesson.objects.filter(product__in=accessible_products)


class ProductLessonDetailView(RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления связи между продуктом и уроком."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProductLessonSerializer

    def get_queryset(self):
        user = self.request.user
        accessible_products = ProductAccess.objects.filter(user=user).values_list('product', flat=True)
        return ProductLesson.objects.filter(product__in=accessible_products)


class LessonViewCreateView(CreateAPIView):
    """Представление для создания записи о просмотре урока пользователем."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LessonViewSerializer


class LessonViewListView(ListAPIView):
    """Представление для просмотра списка уроков, которые просматривал данный пользователь."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LessonViewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        return LessonView.objects.filter(user=user)


class LessonViewDetailView(RetrieveUpdateDestroyAPIView):
    """Представление для получения, обновления и удаления записи о просмотре урока."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LessonViewSerializer

    def get_queryset(self):
        user = self.request.user
        return LessonView.objects.filter(user=user)


class ProductStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_users = User.objects.count()

        products = Product.objects.annotate(
            viewed_lessons_count=Count(
                'productlesson__lesson__lessonview',
                filter=Q(productlesson__lesson__lessonview__view_duration__gte=F('productlesson__lesson__duration') * 0.8),
                distinct=True
            ),
            total_view_time=Sum(
                'productlesson__lesson__lessonview__view_duration',
                filter=Q(productlesson__lesson__lessonview__view_duration__gte=F('productlesson__lesson__duration') * 0.8)
            ),
            students_count=Count('productaccess__user', distinct=True),
            purchase_percentage=ExpressionWrapper(
                Count('productaccess__user', distinct=True) * 100.0 / total_users,
                output_field=FloatField()
            )
        )

        data = [
            {
                "id_продукта": product.id,
                "название продукта": product.name,
                "количество просмотренных уроков": product.viewed_lessons_count,
                "общее время просмотра": product.total_view_time,
                "количество студентов": product.students_count,
                "процент приобретения": product.purchase_percentage
            }
            for product in products
        ]

        return Response(data)