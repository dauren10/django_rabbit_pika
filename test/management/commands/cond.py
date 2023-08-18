from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, **_: dict) -> None:
        connected = False
        print(111)