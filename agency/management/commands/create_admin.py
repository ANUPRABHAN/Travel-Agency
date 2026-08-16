from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create or update the admin user"

    def handle(self, *args, **kwargs):
        username = "admin"
        password = "2026admin"
        email = "admin@combass.com"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            }
        )

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS("Admin user created successfully.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Admin user password updated successfully.")
            )