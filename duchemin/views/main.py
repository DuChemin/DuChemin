import datetime

import httplib2
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_change
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from duchemin.forms.analysis_form import AnalysisForm
from duchemin.models.piece import DCPiece
from duchemin.models.phrase import DCPhrase
from duchemin.models.analysis import DCAnalysis
from duchemin.models.comment import DCComment
from duchemin.models.reconstruction import DCReconstruction
from duchemin.models.content_block import DCContentBlock


def home(request):
    front_page_blocks = DCContentBlock.objects.filter(published=True, content_type="block").order_by('position')
    front_page_blocks = front_page_blocks[0:3]
    news_blocks = DCContentBlock.objects.filter(published=True, content_type="news").order_by('position')
    is_logged_in = False
    if request.user.is_authenticated():
        is_logged_in = True
    data = {
        'user': request.user,
        'front_page_blocks': front_page_blocks,
        'news_blocks': news_blocks,
        'is_logged_in': is_logged_in
    }
    return render(request, 'main/home.html', data)

@login_required(login_url="/login/")
def profile(request):
    profile = request.user.profile

    analyses = None
    reconstructions = None
    discussed_pieces = []

    if profile.person:
        analyses = DCAnalysis.objects.filter(analyst=profile.person.person_id).order_by('composition_number')
        reconstructions = DCReconstruction.objects.filter(reconstructor=profile.person.person_id).order_by('piece')

    comments_by_piece_id = DCComment.objects.filter(author=request.user).order_by('piece')
    for comment in comments_by_piece_id:
        if comment.piece not in discussed_pieces:
            discussed_pieces.append(comment.piece)

    pieces_with_notes = []
    # for piece in DCPiece.objects.all().order_by('piece_id'):
    #     if notetext(request.user, piece):
    #         pieces_with_notes.append(piece)

    data = {
        'user': request.user,
        'profile': profile,
        'favourited_pieces': profile.favourited_piece.order_by('piece_id'),
        'favourited_analyses': profile.favourited_analysis.order_by('piece_id'),
        'favourited_reconstructions': profile.favourited_reconstruction.order_by('piece'),
        'my_analyses': analyses,
        'my_reconstructions': reconstructions,
        'my_comments': DCComment.objects.filter(author=request.user).order_by('-created'),
        'discussed_pieces': discussed_pieces,
        'pieces_with_notes': pieces_with_notes,
        }
    return render(request, 'main/profile.html', data, context_instance=RequestContext(request))


# DEBUGGING
def pass_to_mei(request):
    h = httplib2.Http()
    _, content = h.request("http://digitalduchemin.org/mei/DC0101.xml", "GET", headers={'content-type': 'application/xml'})
    resp = HttpResponse(content)
    resp["Content-Type"] = "application/xml"
    return resp


@login_required(login_url="/login/")
def my_password_change(request):
    return password_change(request, template_name='registration/password_change_form.html',
        post_change_redirect="/profile/",)


@login_required(login_url="/login/")
def add_observation(request, piece_id):
    # Redirect to url with uppercase piece ID
    if piece_id != piece_id.upper():
        return HttpResponseRedirect("/piece/{0}/add-observation/".format(piece_id.upper()))
    # return render(request, 'main/add_analysis.html', {})
    try:
        piece = DCPiece.objects.get(piece_id=piece_id)
    except DCPiece.DoesNotExist:
        raise Http404
    if request.method == "POST":
        form_data = AnalysisForm(request.POST)
        if not form_data.is_valid():
            return render(request, 'main/add_observation.html', {'form': form_data, 'piece': piece})

        #process data in form.cleaned_data()
        earlier_phrase = form_data.cleaned_data.get('earlier_phrase', None)
        if earlier_phrase:
            form_data.cleaned_data['earlier_phrase'] = earlier_phrase.phrase_num

        cadence_alter = form_data.cleaned_data.get('cadence_alter', None)
        if cadence_alter:
            if "Other" in cadence_alter:
                cadence_alter = [c for c in cadence_alter if c != "Other"]
                cadence_alter.append(form_data.cleaned_data.get('cadence_alter_other', None))
            form_data.cleaned_data['cadence_alter'] = ", ".join(cadence_alter)
        else:
            form_data.cleaned_data['cadence_alter'] = ""
        del form_data.cleaned_data['cadence_alter_other']

        other_contrapuntal = form_data.cleaned_data.get('other_contrapuntal', None)
        print "Other: ", other_contrapuntal
        if other_contrapuntal:
            if "Other" in other_contrapuntal:
                other_contrapuntal = [c for c in other_contrapuntal if c != "Other"]
                other_contrapuntal.append(form_data.cleaned_data.get('other_contrapuntal_other', None))
            form_data.cleaned_data['other_contrapuntal'] = ", ".join(other_contrapuntal)
        else:
            form_data.cleaned_data['other_contrapuntal'] = ""

        del form_data.cleaned_data['other_contrapuntal_other']

        other_formulas = form_data.cleaned_data.get('other_formulas', None)
        if other_formulas:
            form_data.cleaned_data['other_formulas'] = "".join(other_formulas)  # right now this is only one item, Romanesca.
        else:
            form_data.cleaned_data['other_formulas'] = ""

        text_treatment = form_data.cleaned_data.get('text_treatment', None)
        if text_treatment == "Other":
            other_description = form_data.cleaned_data.get("text_treatment_other", None)
            if not other_description:
                # raise a form validation error
                pass
            text_treatment = other_description
        del form_data.cleaned_data['text_treatment_other']

        form_data.cleaned_data['composition_number'] = piece
        form_data.cleaned_data['analyst'] = request.user.profile.person
        form_data.cleaned_data['needs_review'] = True
        tstamp = datetime.datetime.now()
        form_data.cleaned_data['timestamp'] = tstamp.strftime("%d/%m/%Y %H:%M:%S")

        # more form cleaning here.
        analysis = DCAnalysis(**form_data.cleaned_data)
        analysis.save()

        return HttpResponseRedirect('/piece/' + piece_id)
    else:
        form_data = AnalysisForm()
        phrases_for_piece = DCPhrase.objects.filter(piece_id=piece_id).order_by('phrase_num')
        form_data.fields['phrase_number'].queryset = phrases_for_piece
        form_data.fields['earlier_phrase'].queryset = phrases_for_piece
        # phrases = DCPhrase.objects.filter(piece_id=piece_id).order_by('phrase_num')
    return render(request, 'main/add_observation.html', {'form': form_data, 'piece': piece})
