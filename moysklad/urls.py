from django.urls import path

from moysklad import views

app_name = "moysklad"
urlpatterns = [
    path('auth', views.auth, name='auth'),
    path('get_products/', views.get_products, name='get_products'),
    path('get_products/<int:id>', views.get_products, name='get_products_with_id'),
    path('check_connection/<int:id>', views.check_connection, name='check_connection'),
]
