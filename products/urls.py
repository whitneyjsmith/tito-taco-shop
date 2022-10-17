from products import views
from django.urls import path


urlpatterns = [
    path('<int:product_id>/', views.product, name='product-page'),
    path('<int:product_id>/product_images/<str:filename>', views.get_image, name='product-img'),
    path('checkout/', views.checkout, name='checkout-page'), # TODO: need to add user id to url pattern
]