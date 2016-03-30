import csv

from django.core.management.base import BaseCommand, CommandError

from collector.utils import add_share


class Command(BaseCommand):
    help = 'Import Shares'

    def add_arguments(self, parser):
        parser.add_argument('file_path')

    def handle(self, *args, **options):
        file_path = options['file_path']
        msg = 'Importing shares from {}'.format(file_path)
        self.stdout.write(self.style.NOTICE(msg))

        with open(file_path) as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                symbol = row.get('symbol')
                if symbol:
                    msg = 'Adding data for {}'.format(symbol)
                    self.stdout.write(msg)
                    try:
                        add_share(symbol)
                    except ValueError:
                        msg = 'Unable to find data for {}'.format(symbol)
                        self.stdout.write(self.style.NOTICE(msg))

        self.stdout.write(self.style.SUCCESS('Done.'))

