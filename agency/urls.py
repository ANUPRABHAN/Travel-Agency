from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),

    path(
        'admin-login/',
        views.admin_login,
        name='admin_login'
    ),

    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'admin-logout/',
        views.admin_logout,
        name='admin_logout'
    ),

    # Package Management

    path(
        'admin-packages/add/',
        views.add_package,
        name='add_package'
    ),

    path(
        'admin-packages/edit/<int:package_id>/',
        views.edit_package,
        name='edit_package'
    ),

    path(
        'admin-packages/delete/<int:package_id>/',
        views.delete_package,
        name='delete_package'
    ),

    path(
        'package/<int:package_id>/',
        views.package_detail,
        name='package_detail'
    ),

    path(
        'admin-customers/edit/<int:customer_id>/',
        views.edit_customer,
        name='edit_customer'
    ),

    path(
        'admin-customers/delete/<int:customer_id>/',
        views.delete_customer,
        name='delete_customer'
    ),
]