from django.db import migrations
from django.db.models import F
from django.db.models.functions import Replace
from django.db.models import Value


def update_pdf_links(apps, schema_editor):
    DCPiece = apps.get_model('duchemin', 'DCPiece')
    DCPiece.objects.filter(pdf_link__startswith='http://ricercar').update(
        pdf_link=Replace(F('pdf_link'), Value('http://ricercar'), Value('ricercar-old'))
    )


class Migration(migrations.Migration):

    dependencies = [
        ('duchemin', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_pdf_links, migrations.RunPython.noop),
    ]
