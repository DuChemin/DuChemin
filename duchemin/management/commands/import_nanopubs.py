from django.core.management.base import BaseCommand
from optparse import make_option
import csv

from duchemin.models import DCAnalysis

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--pubs',
            action='store',
            dest='pubs',
            default=False,
            help='Path to Nanopubs CSV file'
        ),
    )

    def handle(self, *args, **options):
        csvopt = options.get('pubs', False)

        if not csvopt:
            print('You must specify a CSV file.')
            import sys
            sys.exit(-1)

        with open(csvopt) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                obs = DCAnalysis.objects.get(id=row['observation'])

                if not obs:
                    print('observation {0} could not be found!'.format(row['observation']))
                    continue

                print('Processing observation {0}'.format(obs.id))

                obs.nanopub_link = row['npURI']
                obs.save()
