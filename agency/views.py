from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail

from django.shortcuts import render, redirect, get_object_or_404

from .models import Package, Customer, SiteSettings
from .forms import PackageForm, CustomerForm


# =====================================================
# HOME PAGE
# =====================================================

def main(request):

    packages = Package.objects.filter(
        is_active=True
    ).order_by('-created_at')

    # Get website contact information
    settings_obj, created = SiteSettings.objects.get_or_create(
        id=1,
        defaults={
            'notification_email': 'lucilucifer844@gmail.com',
            'address': '123, Travel Street,\nParadise City,\nIndia - 560001',
            'phone': '+91 98765 43210',
            'contact_email': 'info@combassholiday.com',
            'website': 'www.combassholiday.com',
        }
    )

    if request.method == 'POST':

        form = CustomerForm(request.POST)

        if form.is_valid():

            # ---------------------------------------------
            # SAVE ENQUIRY TO DATABASE
            # ---------------------------------------------

            customer = form.save()

            # ---------------------------------------------
            # GET NOTIFICATION EMAIL
            # ---------------------------------------------

            notification_email = settings_obj.notification_email

            # ---------------------------------------------
            # PACKAGE NAME
            # ---------------------------------------------

            if customer.package:

                package_name = customer.package.destination

            else:

                package_name = "No package selected"

            # ---------------------------------------------
            # EMAIL SUBJECT
            # ---------------------------------------------

            subject = (
                f"New Package Enquiry - {customer.full_name}"
            )

            # ---------------------------------------------
            # EMAIL MESSAGE
            # ---------------------------------------------

            email_message = f"""
New package enquiry received from the Combass Travel Agency website.

----------------------------------------
CUSTOMER DETAILS
----------------------------------------

👤 Name :
{customer.full_name}

📧 Email :
{customer.email}

📞 Mobile :
{customer.mobile}

🌍 Package :
{package_name}

📅 Travel Date :
{customer.travel_date}

Message:
{customer.message}

----------------------------------------

Please log in to the admin dashboard to view
and manage this enquiry.

Combass Holiday Pvt Ltd
"""

            # ---------------------------------------------
            # SEND EMAIL
            # ---------------------------------------------

            try:

                send_mail(
                    subject,
                    email_message,
                    None,
                    [notification_email],
                    fail_silently=False,
                )

                email_sent = True

            except Exception as e:

                print(
                    "EMAIL SENDING ERROR:",
                    e
                )

                email_sent = False

            # ---------------------------------------------
            # SUCCESS MESSAGE
            # ---------------------------------------------

            if email_sent:

                messages.success(
                    request,
                    "Your enquiry has been submitted successfully."
                )

            else:

                messages.success(
                    request,
                    "Your enquiry has been submitted successfully. "
                    "We will contact you soon."
                )

            return redirect('main')

    else:

        form = CustomerForm()

    # ---------------------------------------------
    # SEND DATA TO HOMEPAGE
    # ---------------------------------------------

    return render(
        request,
        'index.html',
        {
            'packages': packages,
            'form': form,
            'site_settings': settings_obj,
        }
    )


# =====================================================
# ADMIN LOGIN
# =====================================================

def admin_login(request):

    # If already logged in as staff, go directly to dashboard
    if request.user.is_authenticated:

        if request.user.is_staff:
            return redirect('admin_dashboard')

        else:
            logout(request)

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if user.is_staff:

                login(request, user)

                return redirect('admin_dashboard')

            else:

                return render(
                    request,
                    'admin_login.html',
                    {
                        'error': 'You do not have administrator permission.'
                    }
                )

        else:

            return render(
                request,
                'admin_login.html',
                {
                    'error': 'Invalid username or password.'
                }
            )

    return render(request, 'admin_login.html')


# =====================================================
# ADMIN DASHBOARD
# =====================================================

@login_required(login_url='admin_login')
def admin_dashboard(request):

    # Only staff users can access dashboard
    if not request.user.is_staff:

        logout(request)

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

@login_required(login_url='admin_login')
def admin_logout(request):

    logout(request)

    return redirect('admin_login')


# =====================================================
# CHANGE ADMIN USERNAME / PASSWORD
# =====================================================

@login_required(login_url='admin_login')
def change_admin_credentials(request):

    # Only staff users can access this page
    if not request.user.is_staff:

        logout(request)

        return redirect('admin_login')

    user = request.user

    if request.method == 'POST':
        print("CHANGE CREDENTIALS POST RECEIVED")

        current_password = request.POST.get(
            'current_password',
            ''
        )

        new_username = request.POST.get(
            'username',
            ''
        ).strip()

        new_password = request.POST.get(
            'new_password',
            ''
        )

        confirm_password = request.POST.get(
            'confirm_password',
            ''
        )

        # ---------------------------------------------
        # Check current password
        # ---------------------------------------------

        if not user.check_password(current_password):

            messages.error(
                request,
                'Current password is incorrect.'
            )

            return redirect('change_admin_credentials')


        # ---------------------------------------------
        # Check username
        # ---------------------------------------------

        if not new_username:

            messages.error(
                request,
                'Username cannot be empty.'
            )

            return redirect('change_admin_credentials')


        # ---------------------------------------------
        # Check whether username already exists
        # ---------------------------------------------

        username_exists = User.objects.filter(
            username=new_username
        ).exclude(
            id=user.id
        ).exists()

        if username_exists:

            messages.error(
                request,
                'This username is already being used.'
            )

            return redirect('change_admin_credentials')


        # ---------------------------------------------
        # Check password
        # ---------------------------------------------

        if new_password:

            if len(new_password) < 8:

                messages.error(
                    request,
                    'New password must contain at least 8 characters.'
                )

                return redirect('change_admin_credentials')


            if new_password != confirm_password:

                messages.error(
                    request,
                    'New passwords do not match.'
                )

                return redirect('change_admin_credentials')


        # ---------------------------------------------
        # Update username
        # ---------------------------------------------

        user.username = new_username


        # ---------------------------------------------
        # Update password if provided
        # ---------------------------------------------

        if new_password:

            user.set_password(new_password)


        user.save()


        # ---------------------------------------------
        # Keep admin logged in
        # ---------------------------------------------

        if new_password:

            update_session_auth_hash(
                request,
                user
            )


        messages.success(
            request,
            'Admin credentials updated successfully.'
        )

        return redirect('admin_dashboard')


    return render(
        request,
        'change_admin_credentials.html'
    )


# =====================================================
# ADD PACKAGE
# =====================================================

@login_required(login_url='admin_login')
def add_package(request):

    if not request.user.is_staff:

        logout(request)

        return redirect('admin_login')

    if request.method == 'POST':

        form = PackageForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Package added successfully.'
            )

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

        logout(request)

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

            messages.success(
                request,
                'Package updated successfully.'
            )

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

        logout(request)

        return redirect('admin_login')

    package = get_object_or_404(
        Package,
        id=package_id
    )

    if request.method == 'POST':

        package.delete()

        messages.success(
            request,
            'Package deleted successfully.'
        )

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

        logout(request)

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

            messages.success(
                request,
                'Customer details updated successfully.'
            )

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

        logout(request)

        return redirect('admin_login')

    customer = get_object_or_404(
        Customer,
        id=customer_id
    )

    if request.method == 'POST':

        customer.delete()

        messages.success(
            request,
            'Customer deleted successfully.'
        )

    return redirect('admin_dashboard')

@login_required(login_url='admin_login')
def admin_settings(request):

    if not request.user.is_staff:

        logout(request)

        return redirect('admin_login')


    # Get the single SiteSettings record
    settings_obj, created = SiteSettings.objects.get_or_create(
        id=1,
        defaults={
            'notification_email': 'lucilucifer844@gmail.com',
            'address': '123, Travel Street,\nParadise City,\nIndia - 560001',
            'phone': '+91 98765 43210',
            'contact_email': 'info@combassholiday.com',
            'website': 'www.combassholiday.com',
        }
    )


    if request.method == 'POST':

        # =============================================
        # EMAIL NOTIFICATION SETTINGS
        # =============================================

        if 'notification_email' in request.POST:

            notification_email = request.POST.get(
                'notification_email',
                ''
            ).strip()


            if not notification_email:

                messages.error(
                    request,
                    'Notification email cannot be empty.'
                )

                return redirect('admin_settings')


            settings_obj.notification_email = notification_email

            settings_obj.save()


            messages.success(
                request,
                'Notification email updated successfully.'
            )

            return redirect('admin_settings')


        # =============================================
        # CONTACT INFORMATION
        # =============================================

        if 'address' in request.POST:

            address = request.POST.get(
                'address',
                ''
            ).strip()

            phone = request.POST.get(
                'phone',
                ''
            ).strip()

            contact_email = request.POST.get(
                'contact_email',
                ''
            ).strip()

            website = request.POST.get(
                'website',
                ''
            ).strip()


            # -----------------------------------------
            # VALIDATION
            # -----------------------------------------

            if not address:

                messages.error(
                    request,
                    'Address cannot be empty.'
                )

                return redirect('admin_settings')


            if not phone:

                messages.error(
                    request,
                    'Phone number cannot be empty.'
                )

                return redirect('admin_settings')


            if not contact_email:

                messages.error(
                    request,
                    'Contact email cannot be empty.'
                )

                return redirect('admin_settings')


            if not website:

                messages.error(
                    request,
                    'Website cannot be empty.'
                )

                return redirect('admin_settings')


            # -----------------------------------------
            # SAVE CONTACT INFORMATION
            # -----------------------------------------

            settings_obj.address = address

            settings_obj.phone = phone

            settings_obj.contact_email = contact_email

            settings_obj.website = website

            settings_obj.save()


            messages.success(
                request,
                'Contact information updated successfully.'
            )

            return redirect('admin_settings')


    return render(
        request,
        'admin_settings.html',
        {
            'settings': settings_obj
        }
    )