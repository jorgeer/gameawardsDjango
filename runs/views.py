from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.template import RequestContext
from django.utils import timezone
from runs.forms import GameRegistrationForm, GameDevForm
from runs.models import Game, Run, Developer
import ayah
from gameawards.utils import sanitizeHtml


def game_registration_request(request):

    ayah_html = ayah.get_publisher_html()
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = GameRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            secret = request.POST['session_secret']
            passed = ayah.score_result(secret)
            if passed:
                g = form.save(commit=False)
                g.added_date = timezone.now()
                g.description = sanitizeHtml(request.POST['description'])
                g.run = get_object_or_404(Run, current_run = True)
                g.leader = request.user
                g.save()
                return HttpResponseRedirect('/members/profile/')
            else:
                context = {'form':form, 'ayah_html':ayah_html}
        else:
            context = {'form':form,'ayah_html':ayah_html}
    else:
        form = GameRegistrationForm()
        context = {'form':form,'ayah_html':ayah_html}
    return render_to_response(
        'runs/register_game.html', 
        context, 
        context_instance=RequestContext(request))




def game_list_request(request):
    curr_run = Run.objects.get(current_run = True)
    game_list = Game.objects.filter(run=curr_run).order_by('-added_date')
    context = {'games':game_list}
    return render_to_response(
        'runs/game_list.html', 
        context, 
        context_instance=RequestContext(request))


def game_edit_request(request, game_id):
    g = Game.objects.get(pk=game_id)
    
    ayah_html = ayah.get_publisher_html()
    
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = GameRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            secret = request.POST['session_secret']
            passed = ayah.score_result(secret)
            if passed:
                try:
                    g.concept_only=form.cleaned_data['concept_only']
                except Error:
                    pass
                g.name=form.cleaned_data['name']
                g.short_desc = form.cleaned_data['short_desc']
                g.description = form.cleaned_data['description']
                g.team = form.cleaned_data['team']
                g.save()
                return HttpResponseRedirect('/members/profile/')
            else:
                context = {'form':form, 'ayah_html':ayah_html}
        else:
            context = {'form':form,'ayah_html':ayah_html}
    else:
        form = GameRegistrationForm(instance=g)
        context = {'form':form,'ayah_html':ayah_html}
    return render_to_response(
        'runs/edit_game.html', 
        context, 
        context_instance=RequestContext(request))


def add_game_dev_request(request, game_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    
    g = Game.objects.get(pk = game_id)
    devs = Developer.objects.filter(game=g)
    if request.method == 'POST':
        form = GameDevForm(request.POST, request.FILES)
        if form.is_valid():
            d = form.save(commit=False)
            d.game = g
            d.user = User.objects.get(username=form.cleaned_data['user'])
            d.save()
            return HttpResponseRedirect('/runs/add_game_dev/'+str(game_id))
        else:
            context = {'form':form, 'devs':devs}
    else:
        form = GameDevForm()
        context = {'form':form,'devs':devs}
    return render_to_response(
        'runs/add_game_dev.html', 
        context, 
        context_instance=RequestContext(request))













