from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    help = "Waits for DB to be available"

    def handle(self, *args, **kwargs):
        self.stdout.write("Waiting for DB...")
        db_up = False
        while not db_up:
            try:
                from django.db import connections

                connections["default"].cursor()
                db_up = True
            except OperationalError:
                self.stdout.write("DB unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("DB is ready!"))
