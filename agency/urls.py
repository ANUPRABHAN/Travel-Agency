from django.urls import path
from . import views


urlpatterns = [

    # =================================================
    # HOME
    # =================================================

    path(
        '',
        views.main,
        name='main'
    ),


    # =================================================
    # ADMIN LOGIN
    # =================================================

    path(
        'admin-login/',
        views.admin_login,
        name='admin_login'
    ),


    # =================================================
    # ADMIN DASHBOARD
    # =================================================

    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),


    # =================================================
    # ADMIN LOGOUT
    # =================================================

    path(
        'admin-logout/',
        views.admin_logout,
        name='admin_logout'
    ),

    # =================================================
    # ADMIN CREDENTIALS
    # =================================================

    path(
    'admin-change-credentials/',
    views.change_admin_credentials,
    name='change_admin_credentials'
),


    # =================================================
    # PACKAGE MANAGEMENT
    # =================================================

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


    # =================================================
    # PACKAGE DETAIL
    # =================================================

    path(
        'package/<int:package_id>/',
        views.package_detail,
        name='package_detail'
    ),


    # =================================================
    # CUSTOMER MANAGEMENT
    # =================================================

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

    path(
        'admin-settings/',
        views.admin_settings,
        name='admin_settings'
    ),
]