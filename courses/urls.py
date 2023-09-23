from django.urls import path
from .views import *



urlpatterns = [
    # Маршруты для продуктов
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductView.as_view(), name='product-detail'),

    # Маршруты для доступов к продуктам
    path('product-access/create/', ProductAccessCreateView.as_view(), name='product-access-create'),
    path('product-access/', ProductAccessListView.as_view(), name='product-access-list'),
    path('product-access/<int:pk>/', ProductAccessView.as_view(), name='product-access-detail'),

    # Маршруты для уроков
    path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', ProductLessonView.as_view(), name='lesson-detail'),

    # Маршруты для связи продуктов и уроков
    path('product-lessons/create/', ProductLessonCreateView.as_view(), name='product-lesson-create'),
    path('product-lessons/', ProductLessonListView.as_view(), name='product-lesson-list'),
    path('product-lessons/<int:pk>/', ProductLessonDetailView.as_view(), name='product-lesson-detail'),

    # Маршруты для просмотров уроков
    path('lesson-views/create/', LessonViewCreateView.as_view(), name='lesson-view-create'),
    path('lesson-views/', LessonViewListView.as_view(), name='lesson-view-list'),
    path('lesson-views/<int:pk>/', LessonViewDetailView.as_view(), name='lesson-view-detail'),

    path('products/statistics/', ProductStatisticsView.as_view(), name='product-statistics'),


]
