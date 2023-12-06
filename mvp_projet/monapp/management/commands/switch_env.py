from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Switches the database environment between development and production'

    def add_arguments(self, parser):
        parser.add_argument('env', type=str, choices=['dev', 'prod'])

    def handle(self, *args, **kwargs):
        env = kwargs['env']
        env_file_path = '.env'

        # Lire le fichier .env et remplacer la valeur de DJANGO_DB_MODE
        with open(env_file_path, 'r') as file:
            lines = file.readlines()

        with open(env_file_path, 'w') as file:
            for line in lines:
                if line.startswith('DJANGO_DB_MODE='):
                    file.write(f'DJANGO_DB_MODE={env}\n')
                else:
                    file.write(line)

        self.stdout.write(self.style.SUCCESS(f'Switched to {env} database'))
