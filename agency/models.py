from django.db import models


class Package(models.Model):

    destination = models.CharField(max_length=100)

    image_url = models.URLField(blank=True)

    days = models.PositiveIntegerField()

    nights = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField(blank=True)

    inclusions = models.TextField(blank=True)

    exclusions = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.destination

class Customer(models.Model):

    full_name = models.CharField(max_length=100)

    mobile = models.CharField(max_length=20)

    email = models.EmailField()

    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customers'
    )

    travel_date = models.DateField()

    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.full_name