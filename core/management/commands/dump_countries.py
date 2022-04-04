from django.core.management.base import BaseCommand

from app.utils.dump_countries import dump_countries


class Command(BaseCommand):
    help = "dumps the countries data to the database"

    def handle(self, *args, **options):
        result = dump_countries()
        if result:
            self.stdout.write(
                self.style.SUCCESS("Successfully dumped countries")
            )
        else:
            self.stdout.write(
                self.style.ERROR("Error while dumping countries")
            )
