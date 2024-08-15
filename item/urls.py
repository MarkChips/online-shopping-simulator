from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductList.as_view(), name='home'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:slug>/edit_review/<int:review_id>', views.review_edit, name='review_edit'),
    path('<slug:slug>/delete_review/<int:review_id>', views.review_delete, name='review_delete'),
]