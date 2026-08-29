from django.db import models


# =====================================================
# TRAVEL PACKAGE
# =====================================================

class Package(models.Model):

    destination = models.CharField(
        max_length=100
    )

    image_url = models.URLField(
        blank=True
    )

    days = models.PositiveIntegerField()

    nights = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField(
        blank=True
    )

    inclusions = models.TextField(
        blank=True
    )

    exclusions = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.destination


# =====================================================
# CUSTOMER ENQUIRY
# =====================================================

class Customer(models.Model):

    full_name = models.CharField(
        max_length=100
    )

    mobile = models.CharField(
        max_length=20
    )

    email = models.EmailField()

    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customers'
    )

    # ---------------------------------------------
    # NEW CLIENT REQUIREMENTS
    # ---------------------------------------------

    no_of_persons = models.PositiveIntegerField(
        default=1
    )

    no_of_days = models.PositiveIntegerField(
        default=1
    )

    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # ---------------------------------------------
    # EXISTING FIELDS
    # ---------------------------------------------

    travel_date = models.DateField()

    message = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name


# =====================================================
# SITE SETTINGS
# =====================================================

class SiteSettings(models.Model):

    notification_email = models.EmailField(
        default='lucilucifer844@gmail.com'
    )

    address = models.TextField(
        default='123, Travel Street,\nParadise City,\nIndia - 560001'
    )

    phone = models.CharField(
        max_length=30,
        default='+91 98765 43210'
    )

    contact_email = models.EmailField(
        default='info@combassholiday.com'
    )

    website = models.CharField(
        max_length=200,
        default='www.combassholiday.com'
    )

    def __str__(self):
        return self.notification_email