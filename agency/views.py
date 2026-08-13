from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Package, Customer
from .forms import PackageForm, CustomerForm


# =====================================================
# HOME PAGE
# =====================================================

def main(request):

    packages = Package.objects.filter(
        is_active=True
    ).order_by('-created_at')

    if request.method == 'POST':

        form = CustomerForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('main')

    else:

        form = CustomerForm()

    return render(
        request,
        'index.html',
        {
            'packages': packages,
            'form': form,
        }
    )


# =====================================================
# ADMIN LOGIN
# =====================================================

def admin_login(request):

    # Already logged-in staff user
    if request.user.is_authenticated:

        if request.user.is_staff:
            return redirect('admin_dashboard')

        # Logged-in but not staff
        return redirect('main')


    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:

            login(request, user)

            return redirect('admin_dashboard')

        return render(
            request,
            'admin_login.html',
            {
                'error': 'Invalid username or password.'
            }
        )

    return render(
        request,
        'admin_login.html'
    )


# =====================================================
# ADMIN DASHBOARD
# =====================================================

@login_required(login_url='admin_login')
def admin_dashboard(request):

    # Only staff users can access dashboard
    if not request.user.is_staff:
        return redirect('admin_login')

    packages = Package.objects.all().order_by('-created_at')

    customers = Customer.objects.select_related(
        'package'
    ).order_by('-created_at')

    return render(
        request,
        'admin_dashboard.html',
        {
            'packages': packages,
            'customers': customers,

            'total_packages': packages.count(),

            'total_customers': customers.count(),
        }
    )


# =====================================================
# ADMIN LOGOUT
# =====================================================

def admin_logout(request):

    if request.method == 'POST':

        logout(request)

    return redirect('admin_login')


# =====================================================
# ADD PACKAGE
# =====================================================

@login_required(login_url='admin_login')
def add_package(request):

    if not request.user.is_staff:
        return redirect('admin_login')

    if request.method == 'POST':

        form = PackageForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('admin_dashboard')

    else:

        form = PackageForm()

    return render(
        request,
        'add_package.html',
        {
            'form': form,
            'is_edit': False
        }
    )


# =====================================================
# EDIT PACKAGE
# =====================================================

@login_required(login_url='admin_login')
def edit_package(request, package_id):

    if not request.user.is_staff:
        return redirect('admin_login')

    package = get_object_or_404(
        Package,
        id=package_id
    )

    if request.method == 'POST':

        form = PackageForm(
            request.POST,
            instance=package
        )

        if form.is_valid():

            form.save()

            return redirect('admin_dashboard')

    else:

        form = PackageForm(
            instance=package
        )

    return render(
        request,
        'add_package.html',
        {
            'form': form,
            'package': package,
            'is_edit': True
        }
    )


# =====================================================
# DELETE PACKAGE
# =====================================================

@login_required(login_url='admin_login')
def delete_package(request, package_id):

    if not request.user.is_staff:
        return redirect('admin_login')

    package = get_object_or_404(
        Package,
        id=package_id
    )

    if request.method == 'POST':

        package.delete()

    return redirect('admin_dashboard')


# =====================================================
# PACKAGE DETAIL
# =====================================================

def package_detail(request, package_id):

    package = get_object_or_404(
        Package,
        id=package_id,
        is_active=True
    )

    return render(
        request,
        'package_detail.html',
        {
            'package': package
        }
    )


# =====================================================
# EDIT CUSTOMER
# =====================================================

@login_required(login_url='admin_login')
def edit_customer(request, customer_id):

    if not request.user.is_staff:
        return redirect('admin_login')

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    if request.method == 'POST':

        form = CustomerForm(
            request.POST,
            instance=customer
        )

        if form.is_valid():

            form.save()

            return redirect('admin_dashboard')

    else:

        form = CustomerForm(
            instance=customer
        )

    return render(
        request,
        'edit_customer.html',
        {
            'form': form,
            'customer': customer
        }
    )


# =====================================================
# DELETE CUSTOMER
# =====================================================

@login_required(login_url='admin_login')
def delete_customer(request, customer_id):

    if not request.user.is_staff:
        return redirect('admin_login')

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    if request.method == 'POST':

        customer.delete()

    return redirect('admin_dashboard')