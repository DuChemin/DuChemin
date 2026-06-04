from django.db import migrations


def fix_pdf_links(apps, schema_editor):
    DCPiece = apps.get_model('duchemin', 'DCPiece')
    for piece in DCPiece.objects.filter(pdf_link__contains='ricercar'):
        parts = piece.pdf_link.split('.cesr.univ-tours.fr', 1)
        if len(parts) == 2:
            piece.pdf_link = 'http://ricercar-old.cesr.univ-tours.fr' + parts[1]
            piece.save()


class Migration(migrations.Migration):

    dependencies = [
        ('duchemin', '0002_update_pdf_links'),
    ]

    operations = [
        migrations.RunPython(fix_pdf_links, migrations.RunPython.noop),
    ]
