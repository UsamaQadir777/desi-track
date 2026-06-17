from django.core.management.base import BaseCommand

from apps.foods.seed import seed_foods


class Command(BaseCommand):
    help = "Seed Pakistani/desi food categories and items."

    def handle(self, *args, **options):
        result = seed_foods()
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded foods. Created: {result['created']}, updated: {result['updated']}."
            )
        )
