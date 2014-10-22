from django.template.defaultfilters import register


@register.filter(name='is_favourite')
def is_favourite(user, piece_id):
    return user.profile.favourited_piece.filter(piece_id=piece_id).exists()
