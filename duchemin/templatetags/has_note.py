from django.template.defaultfilters import register
from duchemin.models.note import DCNote


@register.filter(name='has_note')
def has_note(user, piece_id):
    return DCNote.objects.filter(author=user).filter(piece__piece_id=piece_id).exists()
