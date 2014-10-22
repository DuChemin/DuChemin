from django.template.defaultfilters import register


@register.filter(name='is_favourite')
def is_favourite(user, piece):
    return user.profile.favourited_piece.filter(id=piece.id)
