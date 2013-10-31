from django.shortcuts import render
from django.http import HttpResponse,HttpResponseServerError
from django.utils import simplejson
from django.utils.timezone import utc
from django.utils.datastructures import SortedDict
from django.conf import settings
from django.core.paginator import EmptyPage, InvalidPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from duchemin.helpers.solrsearch import DCSolrSearch
from datetime import datetime

from duchemin.models.piece import DCPiece
from duchemin.models.analysis import DCAnalysis
from duchemin.models.reconstruction import DCReconstruction
from duchemin.models.comment import DCComment


class JsonResponse(HttpResponse):
    def __init__(self, content, mimetype='application/json', status=None, content_type=None):
        super(JsonResponse, self).__init__(
            content=simplejson.dumps(content),
            mimetype=mimetype,
            status=status,
            content_type=content_type
        )


@login_required
def favourite_callback(request, ftype, fid):
    action = None
    if 'remove' in request.GET.keys():
        action = 'remove'
    else:
        action = 'add'

    user_profile = request.user.get_profile()

    success = False
    if ftype == 'piece':
        if action == 'remove':
            piece = DCPiece.objects.get(piece_id=fid)
            user_profile.favourited_piece.remove(piece)
            success = True
        else:
            # favourite a piece
            piece = DCPiece.objects.get(piece_id=fid)
            user_profile.favourited_piece.add(piece)
            success = True

    elif ftype == 'analysis':
        if action == 'remove':
            an = DCAnalysis.objects.get(piece_id=fid)
            user_profile.favourited_analysis.remove(an)
            success = True
        else:
            # favourite an analysis
            an = DCAnalysis.objects.get(piece_id=fid)
            user_profile.favourited_analysis.add(an)
            success = True

    elif ftype == 'reconstruction':
        if action == 'remove':
            recon = DCReconstruction.objects.get(piece_id=fid)
            user_profile.favourited_reconstruction.remove(recon)
            success = True
        else:
            recon = DCReconstruction.objects.get(piece_id=fid)
            user_profile.favourited_reconstruction.add(recon)
            success = True
    else:
        pass

    data = {
        'action': action,
        'success': success,
        'content': ftype + "/" + fid
    }
    return JsonResponse(data)


# Callback function to handle returning comments as JSON arrays
# and add new comments using AJAX POST data
@login_required
def discussion_callback(request):

    # TODO: Add csrf_token support to protect from cross-site exploits

    # assuming GET means get comments; POST means add a new one
    if request.method == u'GET':
        get_data = request.GET
        if get_data.has_key('piece_id') and get_data.has_key('last_update'):
            piece_id = get_data['piece_id']
            last_update = get_data['last_update']

            # only return the queryset of objects for this piece newer than
            # the last id (sent from AJAX callback). This assumes a sequential
            # addition of comments, incrementing the id every time
            comments = DCComment.objects.filter(
                piece = DCPiece.objects.get(piece_id=piece_id),
                id__gt = last_update
                )
            comment_array = []
            for comment in comments.values():

                display_time = comment['time'].strftime("%d/%m/%y %H:%M")

                comment_array.append({
                    'id' : u"{}".format(comment['id']),
                    'text' : u"{}".format(comment['text']),
                    'display_time' : u"{}".format(display_time),
                    'author' : u"{}".format(
                        User.objects.get(id=comment['author_id'])),
                })
            return HttpResponse(simplejson.dumps(comment_array),
                mimetype='application/json')
        else:
            return HttpResponseServerError("Missing critical GET attributes")
    elif request.method == u'POST':
        post_data = request.POST
        if post_data.has_key('piece_id') and post_data.has_key('text'):
            piece = DCPiece.objects.get(piece_id=post_data['piece_id'])
            comment = DCComment(author = request.user,
                piece = piece,text = post_data['text'])
            comment.save()
            return HttpResponse("OK!")
        else:
            return HttpResponseServerError("Missing critical POST attributes")


def result_callback(request, restype):
    if restype == 'work':
        return _fetch_work_results(request)
    elif restype == 'element':
        return _fetch_element_results(request)
    elif restype == 'facet':
        return _fetch_facet_results(request)


def _fetch_work_results(request):
    s = DCSolrSearch(request)
    work_res = s.group_search(['title'], fq=['type:(duchemin_analysis OR duchemin_piece)'])

    if work_res.count == 0:
        return render(request, 'search/no_results.html')

    try:
        wpage = int(request.GET.get('wpage', '1'))
    except ValueError:
        wpage = 1

    try:
        work_results = work_res.page(wpage)
    except (EmptyPage, InvalidPage):
        work_results = work_res.page(work_res.num_pages)
    work_results.pager_id = 'works'

    is_logged_in = False
    if request.user.is_authenticated():
        is_logged_in = True
        profile = request.user.profile
        favourite_pieces = [f[0] for f in profile.favourited_piece.all().values_list('piece_id')]
        print favourite_pieces
        if favourite_pieces:
            for piece in work_results.object_list:
                if piece.piece_id in favourite_pieces:
                    piece.is_favourite = True
                else:
                    piece.is_favourite = False

    data = {
        'work_results': work_results,
        'is_logged_in': is_logged_in
    }
    return render(request, 'search/work_result_list.html', data)


def _fetch_element_results(request):
    s = DCSolrSearch(request)
    el_res = s.search(fq=['type:duchemin_analysis'], sort=['piece_id asc', 'phrase_number asc', 'start_measure asc'])

    if el_res.count == 0:
        return render(request, 'search/no_results.html')

    try:
        epage = int(request.GET.get('epage', '1'))
    except ValueError:
        epage = 1

    try:
        element_results = el_res.page(epage)
    except (EmptyPage, InvalidPage):
        element_results = el_res.page(el_res.num_pages)
    element_results.pager_id = 'elements'

    data = {
        'element_results': element_results
    }
    return render(request, 'search/element_result_list.html', data)


def _fetch_facet_results(request):
    s = DCSolrSearch(request)
    facet_params = {
        'facet_mincount': 1,
    }
    facet_res = s.facets(fq=['type:duchemin_analysis'], **facet_params)
    facets = facet_res.facet_counts['facet_fields']
    # filtered_facets = dict([(k, v) for k, v in facets.iteritems() if k in settings.DISPLAY_FACETS])

    filtered_facets = []
    for k, v in facets.iteritems():
        this_facet = []
        if k not in settings.DISPLAY_FACETS.keys():
            continue
        for facet_value, num in v.iteritems():
            if k == "book_id_title":
                facet_info = facet_value.split("_")
                this_facet.append([facet_info[1], settings.DISPLAY_FACETS[k][0], facet_info[0]])
            else:
                this_facet.append([facet_value, settings.DISPLAY_FACETS[k][0]])

        this_facet.sort()
        filtered_facets.append([settings.DISPLAY_FACETS[k][1], this_facet])

    filtered_facets.sort()

    print filtered_facets

    data = {
        'facet_results': filtered_facets
    }
    return render(request, 'search/facets.html', data)
